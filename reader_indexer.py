from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os

def carregar_ou_criar_indice(pasta_docs="docs", pasta_indice="index_storage"):
    # Modelo leve e eficiente, compatível com Render Free (512MiB)
    embed_model = HuggingFaceEmbedding(model_name="intfloat/e5-small-v2")

    if os.path.exists(pasta_indice):
        storage = StorageContext.from_defaults(persist_dir=pasta_indice)
        return load_index_from_storage(storage, embed_model=embed_model)

    documentos = SimpleDirectoryReader(pasta_docs).load_data()
    indice = VectorStoreIndex.from_documents(documentos, embed_model=embed_model)
    indice.storage_context.persist(persist_dir=pasta_indice)
    return indice
