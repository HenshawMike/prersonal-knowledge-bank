import os
from core import vector_store
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from core.vector_store import get_vector_store
from config.settings import settings

def create_or_update_index():
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Initialize vector store and storage context
    vector_store, storage_context = get_vector_store()
    
    # Check if upload directory is empty
    if not os.listdir(settings.UPLOAD_DIR):
        print("No files found in upload directory. Loading existing index if available.")
        try:
            return VectorStoreIndex.from_vector_store(
                vector_store,
                storage_context=storage_context
            )
        except Exception as e:
            print(f"Could not load existing index: {str(e)}")
            return VectorStoreIndex(nodes=[], storage_context=storage_context)
    
    try:
        # Try to load and index documents
        reader = SimpleDirectoryReader(settings.UPLOAD_DIR)
        documents = reader.load_data()
        
        if documents:
            index = VectorStoreIndex.from_documents(
                documents,
                storage_context=storage_context,
                show_progress=True
            )
            storage_context.persist()
            return index
        else:
            raise ValueError("No valid documents found in the upload directory")
            
    except Exception as e:
        print(f"Error processing documents: {str(e)}")
        try:
            # Fallback to existing index if available
            return VectorStoreIndex.from_vector_store(
                vector_store,
                storage_context=storage_context
            )
        except Exception:
            # If all else fails, return an empty index
            return VectorStoreIndex(nodes=[], storage_context=storage_context)