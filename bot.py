import logging
import asyncio
from aiogram import Bot, Dispatcher
from handlers import register_handlers
from os import getenv

# Configuración básica
API_TOKEN = getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

async def main():
    # Inicializar bot y dispatcher
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    
    # Registrar handlers
    register_handlers(dp)

    # Iniciar el bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
