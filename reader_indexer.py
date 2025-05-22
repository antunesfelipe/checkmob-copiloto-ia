from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
import os

def carregar_ou_criar_indice(pasta_docs="docs", pasta_indice="index_storage"):
    # Se já existe índice salvo, carrega
    if os.path.exists(pasta_indice):
        storage = StorageContext.from_defaults(persist_dir=pasta_indice)
        return load_index_from_storage(storage)
    
    # Senão, lê os documentos da pasta
    documentos = SimpleDirectoryReader(pasta_docs).load_data()
    indice = VectorStoreIndex.from_documents(documentos)
    indice.storage_context.persist(persist_dir=pasta_indice)
    return indice
