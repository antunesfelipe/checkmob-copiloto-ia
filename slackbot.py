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
# import os
# import requests
# from urllib.parse import quote

# def baixar_documentos():
#     base_url = "https://raw.githubusercontent.com/antunesfelipe/checkmob-copiloto-ia/main/documentos/"
#     arquivos = [
#         "A.5.1.1 Política de segurança da informação (vigente - 6_8_24).docx",
#         "CP07 - Information Classification Policy.docx",
#         "Política de Segurança de Servidores.docx"
#     ]
    
#     os.makedirs("docs", exist_ok=True)
    
#     for nome in arquivos:
#         url = base_url + quote(nome)
#         caminho_local = os.path.join("docs", nome.replace(" ", "_"))
        
#         print(f"Baixando {url}...")
#         response = requests.get(url)
#         if response.status_code == 200:
#             with open(caminho_local, "wb") as f:
#                 f.write(response.content)
#             print(f"✅ Baixado: {caminho_local}")
#         else:
#             print(f"❌ Erro ao baixar: {url}")


# from fastapi import FastAPI
# from slack_bolt.adapter.socket_mode import SocketModeHandler
# from slack_bolt import App
# import os
# import threading

# # Inicializa o app do Slack
# slack_app = App(token=os.environ["SLACK_BOT_TOKEN"])

# # Evento: menção no canal público
# @slack_app.event("app_mention")
# def handle_mention(event, say):
#     say("Oi! Copiloto IA está online! 🚀")

# # Evento: mensagem privada (direct message)
# @slack_app.event("message")
# def handle_dm(event, say):
#     if event.get("channel_type") == "im":
#         say("Recebi sua mensagem privada! 🤖")

# # Inicia o bot Slack em thread separada
# def start_socket():
#     handler = SocketModeHandler(slack_app, os.environ["SLACK_APP_TOKEN"])
#     handler.start()

# threading.Thread(target=start_socket, daemon=True).start()

# # API FastAPI para manter o serviço no ar
# app = FastAPI()

# @app.get("/")
# def status():
#     return {"status": "Slackbot rodando com sucesso"}
# import os
# import requests
# from urllib.parse import quote
# from reader_indexer import carregar_ou_criar_indice


# # Função para baixar documentos do GitHub
# def baixar_documentos():
#     base_url = "https://raw.githubusercontent.com/antunesfelipe/checkmob-copiloto-ia/main/documentos/"
#     arquivos = [
#         "A.5.1.1 Política de segurança da informação (vigente - 6_8_24).docx",
#         "CP07 - Information Classification Policy.docx",
#         "Política de Segurança de Servidores.docx"
#     ]
    
#     os.makedirs("docs", exist_ok=True)
    
#     for nome in arquivos:
#         url = base_url + quote(nome)
#         caminho_local = os.path.join("docs", nome.replace(" ", "_"))
        
#         print(f"Baixando {url}...")
#         response = requests.get(url)
#         if response.status_code == 200:
#             with open(caminho_local, "wb") as f:
#                 f.write(response.content)
#             print(f"✅ Baixado: {caminho_local}")
#         else:
#             print(f"❌ Erro ao baixar: {url}")

# # Baixar documentos ao iniciar o app
# baixar_documentos()


# from fastapi import FastAPI
# from slack_bolt.adapter.socket_mode import SocketModeHandler
# from slack_bolt import App
# import threading

# # Inicializa o app do Slack
# slack_app = App(token=os.environ["SLACK_BOT_TOKEN"])

# # Carrega o índice dos documentos
# indice = carregar_ou_criar_indice()
# chat_engine = indice.as_chat_engine()

# # Evento: menção no canal público
# @slack_app.event("app_mention")
# def handle_mention(event, say):
#     texto = event.get("text", "")
#     resposta = chat_engine.chat(texto).response
#     say(resposta)

# # Evento: mensagem privada (direct message)
# @slack_app.event("message")
# def handle_dm(event, say):
#     if event.get("channel_type") == "im":
#         texto = event.get("text", "")
#         resposta = chat_engine.chat(texto).response
#         say(resposta)


# # Inicia o bot Slack em thread separada
# def start_socket():
#     handler = SocketModeHandler(slack_app, os.environ["SLACK_APP_TOKEN"])
#     handler.start()

# threading.Thread(target=start_socket, daemon=True).start()

# # API FastAPI para manter o serviço no ar
# app = FastAPI()

# @app.get("/")
# def status():
#     return {"status": "Slackbot rodando com sucesso"}


import os
import threading
import requests
from urllib.parse import quote

from fastapi import FastAPI
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from reader_indexer import carregar_ou_criar_indice

# Baixar documentos automaticamente
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
        print(f"Baixando {url}...")
        response = requests.get(url)
        if response.status_code == 200:
            with open(caminho_local, "wb") as f:
                f.write(response.content)
            print(f"✅ Baixado: {caminho_local}")
        else:
            print(f"❌ Erro ao baixar: {url}")

baixar_documentos()

# Inicializa FastAPI
app = FastAPI()

# Inicializa Slack app
slack_app = App(token=os.environ["SLACK_BOT_TOKEN"])

# Carrega índice e engine
indice = carregar_ou_criar_indice()
chat_engine = indice.as_chat_engine() if indice else None

# Endpoint de status
@app.get("/")
def status():
    return {"status": "Slackbot rodando com sucesso"}

# Endpoint para forçar criação do índice (temporário)
@app.get("/gerar-indice")
def gerar_indice():
    novo_indice = carregar_ou_criar_indice()
    if novo_indice:
        global indice, chat_engine
        indice = novo_indice
        chat_engine = novo_indice.as_chat_engine()
        return {"status": "Índice criado com sucesso"}
    return {"status": "Erro ao criar índice"}

# Evento: menção em canal público
@slack_app.event("app_mention")
def handle_mention(event, say):
    if chat_engine:
        texto = event.get("text", "")
        resposta = chat_engine.chat(texto).response
        say(resposta)
    else:
        say("❌ O índice ainda não foi carregado. Acesse `/gerar-indice`.")

# Evento: mensagem privada
@slack_app.event("message")
def handle_dm(event, say):
    if event.get("channel_type") == "im":
        if chat_engine:
            texto = event.get("text", "")
            resposta = chat_engine.chat(texto).response
            say(resposta)
        else:
            say("❌ O índice ainda não foi carregado. Acesse `/gerar-indice`.")

# Inicia o Slack Socket
def start_socket():
    handler = SocketModeHandler(slack_app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

threading.Thread(target=start_socket, daemon=True).start()


