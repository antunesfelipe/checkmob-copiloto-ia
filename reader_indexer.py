from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os

def carregar_ou_criar_indice(pasta_docs="docs", pasta_indice="index_storage"):
    # Modelo compatível com Render Free Tier (512MiB)
    embed_model = HuggingFaceEmbedding(model_name="intfloat/e5-small-v2")

    if os.path.exists(pasta_indice):
        try:
            storage = StorageContext.from_defaults(persist_dir=pasta_indice)
            print("[INFO] Índice carregado do armazenamento.")
            return load_index_from_storage(storage, embed_model=embed_model)
        except Exception as e:
            print(f"[ERRO] Falha ao carregar índice existente: {e}")
            return None

    # Se não encontrar índice, exibe mensagem (mas NÃO tenta criar no Render)
    if os.environ.get("RENDER") == "true":
        print("[ERRO] Índice não encontrado e ambiente é o Render. Gere o índice localmente e envie via Git.")
        return None

    try:
        print("[INFO] Nenhum índice encontrado. Criando novo índice localmente...")
        documentos = SimpleDirectoryReader(pasta_docs).load_data()
        indice = VectorStoreIndex.from_documents(documentos, embed_model=embed_model)
        indice.storage_context.persist(persist_dir=pasta_indice)
        print("[INFO] Índice criado e salvo com sucesso.")
        return indice
    except Exception as e:
        print(f"[ERRO] Falha ao criar índice: {e}")
        return None
