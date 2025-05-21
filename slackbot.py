import os
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
API_BACKEND_URL = os.getenv("API_BACKEND_URL")

app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def responder(body, say):
    texto = body["event"]["text"]
    usuario = body["event"]["user"]

    try:
        resposta = requests.post(API_BACKEND_URL, json={"texto": texto}).json()
        mensagem = resposta.get("resposta", "Desculpe, não consegui entender.")
        say(f"<@{usuario}> {mensagem}")
    except Exception as e:
        say(f"Erro ao consultar Copiloto IA: {e}")

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
