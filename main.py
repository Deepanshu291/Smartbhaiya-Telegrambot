import os
import threading
import asyncio
import requests
from flask import Flask, request
from bot import main as bot_main, on_webhook
from dotenv import load_dotenv
import time

load_dotenv()

app = Flask(__name__)

@app.route('/')
def start():
    return "SmartBhaiya Bot is Running 🚀"

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     # This handles the webhook updates received from Telegram
#     return asyncio.run(on_webhook(request))

def run_flask():
    # Flask should be run in the main thread
    port = int(os.getenv("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

def ping_self():
    # Keeps the app alive with a ping
    while True:
        try:
            requests.get("https://smartbhaiya-telegrambot.onrender.com/")
        except Exception as e:
            print("Ping failed:", e)
        time.sleep(300)

def start_bot():
    # Start the bot's webhook setup and start the Flask server
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot_main())  # Set the webhook and process updates

if __name__ == '__main__':
    flaskThread = threading.Thread(target=run_flask)
    flaskThread.start()

    start_bot()  # Start the bot with webhook

    ping_self()  # Keep the app alive by pinging itself



# import os
# from flask import Flask, request
# import threading
# import asyncio
# from bot import main,stop
# import requests
# import time
# from dotenv import load_dotenv

# load_dotenv()

# app = Flask(__name__)


# @app.route('/')
# def start():
#     return "SmartBhaiya Bot is Running 🚀"

# @app.route('/startBot')
# def cmd_start():
#     # start_bot()
#     threading.Thread(target=start_bot).start()
#     return "Initialze SmartBhaiya Bot 🚀"

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     update = request.get_json()
#     print(update)

#     return '', 200

# def start_bot():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(stop())
#     loop.run_until_complete(main())

# def run_flask():
#     port = int(os.getenv("PORT",8000))
#     app.run(host='0.0.0.0',port=port)

# def ping_self():
#     while True:
#         try:
#             requests.get("https://smartbhaiya-telegrambot.onrender.com/")
#         except Exception as e:
#             print("Ping failed:", e)
#         time.sleep(300)

# def set_webhook():
#     """Set the webhook URL for the bot."""
#     TELEGRAM_TOKEN = os.getenv("TOKEN")
#     WEBHOOK_URL = 'https://smartbhaiya-telegrambot.onrender.com//webhook'  # Replace with your actual Render URL

#     webhook_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook?url={WEBHOOK_URL}"
#     response = requests.get(webhook_url)
    
#     print("Webhook set:", response.json())


# if __name__ == '__main__':
#     flaskThread = threading.Thread(target=run_flask)
#     flaskThread.start()

#     set_webhook()

#     start_bot()
#     ping_self()



