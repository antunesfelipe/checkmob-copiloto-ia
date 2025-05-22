import os
import threading
import requests
from urllib.parse import quote

from fastapi import FastAPI
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from reader_indexer import carregar_ou_criar_indice

# 🔽 FastAPI App (mantém o Render rodando)
app = FastAPI()

# 🔽 Slack App
slack_app = App(token=os.environ["SLACK_BOT_TOKEN"])

# 🔽 Baixa os documentos do GitHub
def baixar_documentos():
    base_url = "https://raw.githubusercontent.com/antunesfelipe/checkmob-copiloto-ia/main/documentos/"
    arquivos = [
        "A.5.1.1 Política de segurança da informação (vigente - 6_8_24).docx",
        "CP07 - Information Classification Policy.docx",
        "Política de Segurança de Servidores.docx"
    ]
    os.makedirs("docs", exist_ok=True)
    for nome in arquivos:
        url = base_url + quote(nome)
        caminho_local = os.path.join("docs", nome.replace(" ", "_"))
        if not os.path.exists(caminho_local):
            print(f"Baixando {url}...")
            response = requests.get(url)
            if response.status_code == 200:
                with open(caminho_local, "wb") as f:
                    f.write(response.content)
                print(f"✅ Baixado: {caminho_local}")
            else:
                print(f"❌ Erro ao baixar: {url}")
        else:
            print(f"✅ Já existe: {caminho_local}")

baixar_documentos()

# 🔽 Carrega índice salvo (não tenta gerar no Render)
indice = carregar_ou_criar_indice()
chat_engine = indice.as_chat_engine() if indice else None

# 🔽 Endpoint de status
@app.get("/")
def status():
    return {"status": "Slackbot rodando com sucesso"}

# 🔽 Evento: menção pública
@slack_app.event("app_mention")
def handle_mention(event, say):
    texto = event.get("text", "")
    if chat_engine:
        resposta = chat_engine.chat(texto).response
        say(resposta)
    else:
        say("⚠️ O índice ainda não foi carregado. Suba a pasta `index_storage/` no GitHub.")

# 🔽 Evento: mensagem privada
@slack_app.event("message")
def handle_dm(event, say):
    if event.get("channel_type") == "im":
        texto = event.get("text", "")
        if chat_engine:
            resposta = chat_engine.chat(texto).response
            say(resposta)
        else:
            say("⚠️ O índice ainda não foi carregado. Suba a pasta `index_storage/` no GitHub.")

# 🔽 Inicia o socket do Slack
def start_socket():
    handler = SocketModeHandler(slack_app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

threading.Thread(target=start_socket, daemon=True).start()
