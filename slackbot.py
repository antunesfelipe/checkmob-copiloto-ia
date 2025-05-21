# from fastapi import FastAPI
# from slack_bolt.adapter.socket_mode import SocketModeHandler
# from slack_bolt import App
# import os
# import threading

# # Inicializa o app do Slack
# slack_app = App(token=os.environ["SLACK_BOT_TOKEN"])

# @slack_app.event("app_mention")
# def handle_mention(event, say):
#     say("Oi! Copiloto IA está online! 🚀")

# def start_socket():
#     handler = SocketModeHandler(slack_app, os.environ["SLACK_APP_TOKEN"])
#     handler.start()

# # Inicia o bot Slack em thread separada
# threading.Thread(target=start_socket, daemon=True).start()

# # API FastAPI para manter o serviço no ar
# app = FastAPI()

# @app.get("/")
# def status():
#     return {"status": "Slackbot rodando com sucesso"}
from fastapi import FastAPI
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt import App
import os
import threading

# Inicializa o app do Slack
slack_app = App(token=os.environ["SLACK_BOT_TOKEN"])

# Evento: menção no canal público
@slack_app.event("app_mention")
def handle_mention(event, say):
    say("Oi! Copiloto IA está online! 🚀")

# Evento: mensagem privada (direct message)
@slack_app.event("message")
def handle_dm(event, say):
    if event.get("channel_type") == "im":
        say("Recebi sua mensagem privada! 🤖")

# Inicia o bot Slack em thread separada
def start_socket():
    handler = SocketModeHandler(slack_app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

threading.Thread(target=start_socket, daemon=True).start()

# API FastAPI para manter o serviço no ar
app = FastAPI()

@app.get("/")
def status():
    return {"status": "Slackbot rodando com sucesso"}


