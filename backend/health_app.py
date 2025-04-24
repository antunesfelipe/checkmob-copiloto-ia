# backend/health_app.py
from fastapi import FastAPI
import threading
from backend.onyx.onyxbot.slack.listener import SlackbotHandler

app = FastAPI()

@app.get("/healthcheck")
def health():
    return {"status": "ok"}

def start_slackbot():
    handler = SlackbotHandler()
    while handler.running:
        import time
        time.sleep(1)

threading.Thread(target=start_slackbot, daemon=True).start()
