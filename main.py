import os
from flask import Flask, request
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

@app.route('/startBot')
def cmd_start():
    # start_bot()
    threading.Thread(target=start_bot).start()
    return "Initialze SmartBhaiya Bot 🚀"

@app.route('/webhook', methods=['POST'])
def webhook():
    # This is where the update from Telegram will be sent
    update = request.get_json()
    
    # Process the update (you can call your bot's logic to handle the message)
    # For now, you can print the update for debugging purposes
    print(update)
    
    # Here you should process the incoming update with your bot logic
    # For example:
    # await process_update(update)  # (process_update is a function where you process messages)

    return '', 200

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

def set_webhook():
    """Set the webhook URL for the bot."""
    TELEGRAM_TOKEN = os.getenv("TOKEN")
    WEBHOOK_URL = 'https://smartbhaiya-telegrambot.onrender.com//webhook'  # Replace with your actual Render URL

    webhook_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook?url={WEBHOOK_URL}"
    response = requests.get(webhook_url)
    
    print("Webhook set:", response.json())


if __name__ == '__main__':
    flaskThread = threading.Thread(target=run_flask)
    flaskThread.start()

    set_webhook()

    start_bot()



