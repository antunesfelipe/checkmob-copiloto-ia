from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os

def gerar_indice(pasta_docs="docs", pasta_indice="index_storage"):
    print("[INFO] Iniciando geração do índice...")

    if not os.path.exists(pasta_docs):
        print(f"[ERRO] Pasta de documentos '{pasta_docs}' não encontrada.")
        return

    embed_model = HuggingFaceEmbedding(model_name="intfloat/e5-small-v2")

    documentos = SimpleDirectoryReader(pasta_docs).load_data()
    indice = VectorStoreIndex.from_documents(documentos, embed_model=embed_model)
    indice.storage_context.persist(persist_dir=pasta_indice)

    print(f"[✅] Índice gerado com sucesso em '{pasta_indice}/'.")

if __name__ == "__main__":
    gerar_indice()
