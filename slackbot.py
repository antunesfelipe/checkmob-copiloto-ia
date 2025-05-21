from fastapi import FastAPI
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt import App
import os
import threading

# Slack app
slack_app = App(token=os.environ["SLACK_BOT_TOKEN"])

@slack_app.event("app_mention")
def mention_handler(event, say):
    say("Oi! Copiloto IA está online! 🚀")

def start_socket_mode():
    handler = SocketModeHandler(slack_app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

# FastAPI app só para manter a porta 10000 aberta
api = FastAPI()

@api.get("/")
def root():
    return {"status": "Slackbot rodando com sucesso"}

# Inicia o bot em paralelo
threading.Thread(target=start_socket_mode).start()
