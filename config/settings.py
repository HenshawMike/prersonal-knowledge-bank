import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
    
class Settings:
    OPENROUTER_API_KEY = st.secrets.get("openrouter", {}).get("api_key")
    if not OPENROUTER_API_KEY:
        raise ValueError("OpenRouter API key is required in Streamlit secrets")
    
    OPENROUTER_LLM_MODEL = st.secrets.get("openrouter", {}).get(
        "model_name", 
        "openrouter/openai/gpt-oss-120b:free"
    )

    HF_TOKEN=st.secrets.get("hf_token")

    BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_DIR=os.path.join(BASE_DIR, "data", "uploads")
    CHROMA_DIR=os.path.join(BASE_DIR, "data", "chromaDB")

    COLLECTION_NAME="personal_knowledge_base"

settings=Settings()