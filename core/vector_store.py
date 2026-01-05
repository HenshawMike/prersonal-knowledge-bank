import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from config.settings import settings
import os

def get_vector_store():
   use_persistent = os.path.exists(settings.CHROMA_DIR)
    
   if use_persistent:
        client = chromadb.PersistentClient(path=settings.CHROMA_DIR)
   else:
        # Fallback to in-memory for cloud or missing folder
        client = chromadb.Client()
    # Get or create the collection
   collection = client.get_or_create_collection(
        name=settings.COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}  # Use cosine similarity
    )
    
    # Create the vector store
   vector_store = ChromaVectorStore(chroma_collection=collection)
    
    # Create storage context
   storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
   return vector_store, storage_context