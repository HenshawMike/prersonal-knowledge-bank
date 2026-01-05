import os
from core import vector_store
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from core.vector_store import get_vector_store
from config.settings import settings

def create_or_update_index():
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    vector_store, storage_context = get_vector_store()

    reader = SimpleDirectoryReader(settings.UPLOAD_DIR)
    documents = reader.load_data()

    if documents:
        index = VectorStoreIndex.from_documents(documents,
        storage_context=storage_context,
        show_progress=True)

        storage_context.persist()
        return index
    else:
        try:
            return VectorStoreIndex.from_vector_store(vector_store,storage_context=storage_context)
        except Exception:
            return None