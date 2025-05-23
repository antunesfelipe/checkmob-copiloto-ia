from fastapi import FastAPI
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from reader_indexer import carregar_ou_criar_indice
import os
import threading

app = FastAPI()
slack_app = App(token=os.environ["SLACK_BOT_TOKEN"])

indice = carregar_ou_criar_indice()
chat_engine = indice.as_chat_engine() if indice else None

@app.get("/")
def status():
    return {"status": "Slackbot rodando com sucesso"}

@app.get("/gerar-indice")
def gerar_indice():
    return {"status": "Índice já está no repositório"}

@slack_app.event("app_mention")
def handle_mention(event, say):
    if chat_engine:
        resposta = chat_engine.chat(event.get("text", "")).response
        say(resposta)
    else:
        say("❌ Índice não carregado.")

@slack_app.event("message")
def handle_dm(event, say):
    if event.get("channel_type") == "im":
        if chat_engine:
            resposta = chat_engine.chat(event.get("text", "")).response
            say(resposta)
        else:
            say("❌ Índice não carregado.")

def start_socket():
    handler = SocketModeHandler(slack_app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

threading.Thread(target=start_socket, daemon=True).start()
