import os
from flask import Flask
import threading
import asyncio
from bot import main
import requests
import time
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/')
def start():
    return "SmartBhaiya Bot is Running 🚀"

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

def run_flask():
    port = int(os.getenv("PORT",8000))
    app.run(host='0.0.0.0',port=port)

def ping_self():
    while True:
        try:
            requests.get("https://smartbhaiya-telegrambot.onrender.com/")
        except Exception as e:
            print("Ping failed:", e)
        time.sleep(300)

if __name__ == '__main__':
    flaskThread = threading.Thread(target=run_flask)
    flaskThread.start()

    start_bot()



