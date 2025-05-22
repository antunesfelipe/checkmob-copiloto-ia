from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os

def carregar_ou_criar_indice(pasta_docs="docs", pasta_indice="index_storage"):
    # Modelo leve e compatível com Render Free (512MiB)
    embed_model = HuggingFaceEmbedding(model_name="intfloat/e5-small-v2")

    # Se o índice já foi salvo localmente (e comitado no repositório)
    if os.path.exists(pasta_indice):
        try:
            storage = StorageContext.from_defaults(persist_dir=pasta_indice)
            return load_index_from_storage(storage, embed_model=embed_model)
        except Exception as e:
            print(f"[ERRO] Falha ao carregar índice existente: {e}")
            return None

    # Em produção (Render), nunca tente criar o índice — só local
    print("[INFO] Nenhum índice encontrado. Rode localmente para gerar o índice.")
    return None
