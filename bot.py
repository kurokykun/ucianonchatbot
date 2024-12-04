import logging
import asyncio
from aiogram import Bot, Dispatcher
from handlers import register_handlers
from flask import Flask
from os import getenv
import threading

API_TOKEN = str(getenv('BOT_TOKEN'))
PORT = int(getenv('PORT', 5000))

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

@app.route("/")
def home():
    return "El bot está corriendo", 200

def run_flask():
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)

async def start_bot():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    
    register_handlers(dp)

    await dp.start_polling(bot)


def main():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    asyncio.run(start_bot())

if __name__ == "__main__":
    main()