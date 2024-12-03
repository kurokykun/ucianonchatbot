from aiogram import types, Router, F, Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters import or_f
from matchmaker import MatchMaker

# Crear instancia del emparejador
matchmaker = MatchMaker()

router = Router()  # Router para registrar los handlers

# Máquina de estados para controlar el flujo
class UserState(StatesGroup):
    PENDING = State()  # Esperando ser emparejado
    MATCHED = State()  # Emparejado y en conversación
    PREFERENCE = State()  # Para almacenar la preferencia de conversación del usuario

# Comando /start para iniciar el flujo
@router.message(Command("start"))
async def start_command(message: types.Message):
    """Maneja el comando /start."""  
    # Restablecer cualquier estado anterior
    await message.answer(
        "¡Bienvenido al chat anónimo! Por favor, selecciona con quién deseas chatear:\n"
        "1️⃣ Chicos\n"
        "2️⃣ Chicas\n",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Chicos"), KeyboardButton(text="Chicas")],
        ], resize_keyboard=True),
    )


@router.message(or_f(F.text=='/search',F.text=='Buscar'))
async def start_command(message: types.Message):
    """Maneja el comando /search."""  
    # Restablecer cualquier estado anterior
    await message.answer(
        "Por favor, selecciona con quién deseas chatear:\n"
        "1️⃣ Chicos\n"
        "2️⃣ Chicas\n",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Chicos"), KeyboardButton(text="Chicas")],
        ], resize_keyboard=True),
    )

@router.message(Command("config"))
async def start_command(message: types.Message,state: FSMContext):
    """Maneja el comando /search."""  
    # Restablecer cualquier estado anterior
    user_data = await state.get_data()
    gender = user_data.get("preference", "sin preferencia")
    is_male= "✅" if gender == "chicos" else " "
    is_female= "✅" if gender == "chicas" else " "
    is_unknown=" " if gender == "chicos" else " " if gender == "chicas" else "✅"

    await message.answer(
        f"Configuraciones asociadas al bot\n"
        "\n"
        f"Actualmente buscas:\n"
        f"Chicos {is_male}\n"
        f"Chicas {is_female}\n"
        f"No definido {is_unknown}\n",
        
    )

# Configurar preferencia del usuario y registrar estado
@router.message(F.text.in_({"Chicos", "Chicas"}))
async def set_preference(message: types.Message, state: FSMContext):
    """Configura la preferencia del usuario y añade a la cola."""  
    user_id = message.from_user.id
    gender = message.text.lower()

    # Verificar si el usuario ya está en una conversación activa
    if matchmaker.get_partner(user_id):
        await message.answer("Ya estás en una conversación activa. Usa /end para finalizarla primero.")
        return

    # Guardar la preferencia en el estado FSM
    await state.update_data(preference=gender)

    # Agregar a la cola según preferencia
    matchmaker.add_to_queue(user_id, gender)

    # Establecer el estado del usuario como "PENDING"
    await state.set_state(UserState.PENDING)
    
    await message.answer(
        "¡Perfecto! Te hemos añadido a la cola. Espera mientras encontramos a alguien compatible.Puedes utilizar el comando /cancel para detener este proceso",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Cancelar")],
        ],resize_keyboard=True
    )
    )
    # Intentar emparejar al usuario
    partner_id = matchmaker.find_match(user_id, gender)
    if partner_id:
        # Iniciar conversación si hay un match
        await notify_match(message.bot, user_id, partner_id, state)

async def notify_match(bot: Bot, user_id: int, partner_id: int, state: FSMContext):
    """Notifica a ambos usuarios que han sido emparejados."""  
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Siguiente"), KeyboardButton(text="Salir")],
    ], resize_keyboard=True)

    await bot.send_message(user_id, "¡Hemos encontrado un compañero/a! Empieza a chatear ahora. Para finalizar en cualquier momento utiliza el botón de Finalizar o puede escribir /end.", reply_markup=keyboard)
    await bot.send_message(partner_id, "¡Hemos encontrado un compañero/a! Empieza a chatear ahora. Para finalizar en cualquier momento utiliza el botón de Finalizar o puede escribir /end.", reply_markup=keyboard)
    
    # Establecer el estado de ambos usuarios como "MATCHED"
    await state.set_state(UserState.MATCHED)
    matchmaker.start_conversation(user_id, partner_id)

# Handler para el comando "Siguiente"
@router.message(or_f(F.text == "Siguiente",F.text =="/next"))
async def next_match(message: types.Message, state: FSMContext):
    """Busca un nuevo emparejamiento basado en la preferencia almacenada."""  
    user_id = message.from_user.id
    
    # Obtener la preferencia guardada en el estado FSM
    user_data = await state.get_data()
    gender = user_data.get("preference")

    if not gender:
        await message.answer("No has seleccionado una preferencia. Usa /start para configurarla.")
        return

    # Verificar si el usuario ya está en una conversación activa
    if matchmaker.get_partner(user_id):
        

        """Finaliza la conversación actual."""  
        user_id = message.from_user.id

        # Obtener el partner de la conversación
        partner_id = matchmaker.end_conversation(user_id)
        if partner_id:
            await message.bot.send_message(partner_id, "Tu compañero/a ha salido de la conversación. Usa /start para buscar otra conversación.",reply_markup=ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text="Buscar")],
            ],resize_keyboard=True
        ))
        await message.answer(
        "¡Perfecto! Te hemos añadido a la cola. Espera mientras encontramos a alguien compatible.Puedes utilizar el comando /cancel para detener este proceso",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Cancelar")],
        ],resize_keyboard=True
    )
    )
        
        # Restablecer el estado del usuario
        await state.clear()

    # Agregar a la cola de nuevo
    matchmaker.add_to_queue(user_id, gender)

    # Intentar emparejar al usuario
    partner_id = matchmaker.find_match(user_id, gender)
    if partner_id:
        # Iniciar conversación si hay un match
        await notify_match(message.bot, user_id, partner_id, state)


# Comando /end para finalizar la conversación
@router.message(or_f(F.text == "/end",F.text == "Salir"))
async def end_conversation(message: types.Message, state: FSMContext):
    """Finaliza la conversación actual."""  
    user_id = message.from_user.id

    # Obtener el partner de la conversación
    partner_id = matchmaker.end_conversation(user_id)
    if partner_id:
        await message.bot.send_message(partner_id, "Tu compañero/a ha salido de la conversación. Usa /start para buscar otra conversación.",reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Buscar")],
        ],resize_keyboard=True
    ))
    await message.answer("Has salido de la conversación. Usa /start para buscar otra conversación.",reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Buscar")],
        ],resize_keyboard=True
    ))
    
    # Restablecer el estado del usuario
    await state.clear()

@router.message(or_f(F.text == "/cancel" , F.text == "Cancelar"))
async def cancel_queue(message: types.Message, state: FSMContext):
    """Maneja la cancelación de la cola de espera."""  
    user_id = message.from_user.id

    # Verificar si el usuario está esperando en la cola (estado "PENDING")
    user_data = await state.get_data()
    if not user_data.get("preference"):
        await message.answer("No estás en la cola de espera. Usa /start para comenzar.")
        return

    # Eliminar al usuario de la cola
    matchmaker.remove_from_queue(user_id)

    # Restablecer el estado del usuario
    await state.clear()

    # Informar al usuario que se ha cancelado
    await message.answer("Has cancelado tu solicitud de emparejamiento. Puedes usar /start para volver a empezar.",reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Buscar")],
        ],resize_keyboard=True
    ))


# Handler para enviar mensajes dentro de la conversación
@router.message()
async def relay_message(message: types.Message):
    """Reenvía los mensajes al compañero de conversación, incluyendo multimedia."""

    user_id = message.from_user.id
    partner_id = matchmaker.get_partner(user_id)

    if partner_id:
        # Si el mensaje es una respuesta a otro, el bot también responderá al mensaje original
        if message.reply_to_message:
            # Verificar si el mensaje al que se está respondiendo es de nuestro compañero
            if message.reply_to_message.from_user.id == partner_id:
                # El mensaje al que se está respondiendo es del compañero
                if message.text:
                    await message.bot.send_message(
                        partner_id, 
                        message.text, 
                        reply_to_message_id=message.reply_to_message.message_id
                    )
                elif message.photo:
                    await message.bot.send_photo(
                        partner_id, 
                        message.photo[-1].file_id,  # Selecciona la mejor calidad de la foto
                        caption=message.caption,  # Si tiene un pie de foto
                        reply_to_message_id=message.reply_to_message.message_id
                    )
                elif message.video:
                    await message.bot.send_video(
                        partner_id, 
                        message.video.file_id,
                        caption=message.caption,  # Si tiene un pie de foto
                        reply_to_message_id=message.reply_to_message.message_id
                    )
                elif message.audio:
                    await message.bot.send_audio(
                        partner_id, 
                        message.audio.file_id,
                        caption=message.caption,  # Si tiene un pie de foto
                        reply_to_message_id=message.reply_to_message.message_id
                    )
                elif message.document:
                    await message.bot.send_document(
                        partner_id, 
                        message.document.file_id,
                        caption=message.caption,  # Si tiene un pie de foto
                        reply_to_message_id=message.reply_to_message.message_id
                    )
                else:
                    # Si es otro tipo de contenido multimedia no manejado, enviar un mensaje
                    await message.bot.send_message(
                        partner_id, 
                        "Mensaje con formato no soportado.", 
                        reply_to_message_id=message.reply_to_message.message_id
                    )
            else:
                # El mensaje al que se está respondiendo no es del compañero (puede ser del bot)
                # Enviar el mensaje sin "reply_to_message_id"
                if message.text:
                    await message.bot.send_message(partner_id, message.text)
                elif message.photo:
                    await message.bot.send_photo(
                        partner_id, 
                        message.photo[-1].file_id,  # Selecciona la mejor calidad de la foto
                        caption=message.caption
                    )
                elif message.video:
                    await message.bot.send_video(
                        partner_id, 
                        message.video.file_id,
                        caption=message.caption
                    )
                elif message.audio:
                    await message.bot.send_audio(
                        partner_id, 
                        message.audio.file_id,
                        caption=message.caption
                    )
                elif message.document:
                    await message.bot.send_document(
                        partner_id, 
                        message.document.file_id,
                        caption=message.caption
                    )
                else:
                    # Si es otro tipo de contenido multimedia no manejado, enviar un mensaje
                    await message.bot.send_message(partner_id, "Mensaje con formato no soportado.")
        else:
            # Si no es una respuesta directa, simplemente reenvía el mensaje
            if message.text:
                await message.bot.send_message(partner_id, message.text)
            elif message.photo:
                await message.bot.send_photo(
                    partner_id, 
                    message.photo[-1].file_id,  # Selecciona la mejor calidad de la foto
                    caption=message.caption
                )
            elif message.video:
                await message.bot.send_video(
                    partner_id, 
                    message.video.file_id,
                    caption=message.caption
                )
            elif message.audio:
                await message.bot.send_audio(
                    partner_id, 
                    message.audio.file_id,
                    caption=message.caption
                )
            elif message.document:
                await message.bot.send_document(
                    partner_id, 
                    message.document.file_id,
                    caption=message.caption
                )
            else:
                # Si es otro tipo de contenido multimedia no manejado, enviar un mensaje
                await message.bot.send_message(partner_id, "Mensaje con formato no soportado.")
    else:
        # Si no hay compañero en la conversación, notifica al usuario
        await message.answer("No estás en una conversación activa. Usa /start para comenzar de nuevo.")

# Registrar los handlers
def register_handlers(dp: Dispatcher):
    """Registra todos los handlers en el dispatcher."""  
    dp.include_router(router)
