import logging
import asyncio
from aiogram import Bot, Dispatcher
from handlers import register_handlers
from flask import Flask, request

import os

# Configuración básica
API_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
app = Flask(__name__)

async def on_startup():
    # Configurar comandos y webhook al iniciar
    RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")
    register_handlers(dp)
    if not RENDER_EXTERNAL_URL:
        raise ValueError("RENDER_EXTERNAL_URL no está definido en las variables de entorno.")
    webhook_url = f"{RENDER_EXTERNAL_URL}/{API_TOKEN}"
    await bot.set_webhook(webhook_url)
    print(f"Webhook configurado en: {webhook_url}")

async def on_shutdown():
    # Eliminar el webhook al apagar
    await bot.delete_webhook()
    await bot.session.close()

if __name__ == "__main__":
    # Configurar el servidor Flask y ejecutar Aiogram en paralelo
    PORT = int(os.environ.get("PORT", 5000))

    # Crear un bucle de eventos de asyncio para ejecutar Flask y tareas de Aiogram
    loop = asyncio.get_event_loop()

    # Agregar tareas para on_startup y on_shutdown
    loop.run_until_complete(on_startup())
    try:
        app.run(host="0.0.0.0", port=PORT, threaded=False)  # Flask debe ejecutarse en el hilo principal
    except KeyboardInterrupt:
        loop.run_until_complete(on_shutdown())