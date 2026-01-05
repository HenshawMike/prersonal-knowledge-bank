from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import ContextChatEngine
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings    
from llama_index.core import Settings as LlamaSettings
from config.settings import settings
from core.embeddings import CachedHuggingFaceEmbeddings


    

LlamaSettings.embed_model = CachedHuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L12-v2",
            api_base="https://router.huggingface.co",
            api_key=settings.HF_TOKEN)

LlamaSettings.llm = OpenAI(api_key=settings.OPENROUTER_API_KEY,
                        model_name=settings.OPENROUTER_LLM_MODEL,
                        api_base="https://openrouter.ai/api/v1",
                        temperature=0.7) 

def get_chat_engine(index):
    if not index:
        return None

    memory= ChatMemoryBuffer.from_defaults(token_limit=4000)

    chat_engine= ContextChatEngine.from_defaults(retriever=index.as_retriever(similarity_top_k=6),
    memory=memory,
    system_prompt=("You are a warm, insightful assistant that answers from the user's personal knowledge. "
                 "Be accurate, concise, and friendly. If unsure, say 'I don't see that in your notes.'"
                 ))
    return chat_engine


__all__ =['chat_engine']