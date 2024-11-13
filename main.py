from flask import Flask
import threading
import asyncio
from bot import main

app = Flask(__name__)

@app.route('/')
def start():
    return "SmartBhaiya Bot is Running 🚀"

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

def run_flask():
    app.run(host='0.0.0.0',port=8000)

if __name__ == '__main__':
    flaskThread = threading.Thread(target=run_flask)
    flaskThread.start()

    start_bot()


