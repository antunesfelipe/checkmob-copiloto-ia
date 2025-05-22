from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding  # ✅ Caminho correto
import os

def carregar_ou_criar_indice(pasta_docs="docs", pasta_indice="index_storage"):
    # Define modelo local de embedding
    # embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/paraphrase-MiniLM-L3-v2")


    if os.path.exists(pasta_indice):
        storage = StorageContext.from_defaults(persist_dir=pasta_indice)
        return load_index_from_storage(storage, embed_model=embed_model)

    documentos = SimpleDirectoryReader(pasta_docs).load_data()
    indice = VectorStoreIndex.from_documents(documentos, embed_model=embed_model)
    indice.storage_context.persist(persist_dir=pasta_indice)
    return indice
