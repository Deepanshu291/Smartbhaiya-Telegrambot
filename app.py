import os
import threading
import asyncio
from fastapi import FastAPI
from bot import main, stop
import requests
import time
from dotenv import load_dotenv
from uvicorn import Config, Server

load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "SmartBhaiya Bot is Running 🚀"}

@app.get("/startBot")
async def cmd_start():
    # Launch the bot in a separate thread to avoid blocking the server
    threading.Thread(target=start_bot).start()
    return {"message": "Initializing SmartBhaiya Bot 🚀"}

@app.get("/stopBot")
async def cmd_start():
    # Launch the bot in a separate thread to avoid blocking the server
    threading.Thread(target=stop_bot).start()
    return {"message": "Stoping SmartBhaiya Bot 🚀"}

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

def stop_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(stop())

def ping_self():
    """Keeps the server active by pinging it periodically."""
    while True:
        try:
            requests.get("https://smartbhaiya-telegrambot.onrender.com/")
        except Exception as e:
            print("Ping failed:", e)
        time.sleep(300)



if __name__ == "__main__":
    # Start a background thread for periodic self-pinging
    threading.Thread(target=ping_self, daemon=True).start()

    # Start the FastAPI server
    port = int(os.getenv("PORT", 8000))
    config = Config(app=app,host='0.0.0.0', port=port, log_level="info")
    server = Server(config)
    asyncio.run(server.serve())
    ping_self()
