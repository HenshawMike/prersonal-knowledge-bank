import streamlit as st
from ui.sidebar import render as render_sidebar
from ui.chat import render as render_chat
from ui.dashboard import render as render_dashboard
from core.ingestion import create_or_update_index
from core.retriever import get_chat_engine
from core.agents import chat_engine
import asyncio

st.set_page_config(page_title="Personal Knowledge Bank", page_icon="🧠", layout="wide")

st.title("🧠 Personal Knowledge Bank")
st.markdown("*Your private AI second brain — HF Inference embeddings + OpenRouter LLM*")

render_sidebar()

tab_dashboard, tab_chat, tab_agents = st.tabs(["📊 Dashboard", "💬 Chat", "🤖 Agents"])

with tab_dashboard:
    index = create_or_update_index()
    render_dashboard(index)

with tab_chat:
    index = create_or_update_index()
    chat_engine = get_chat_engine(index)
    render_chat(chat_engine)

with tab_agents:
    st.header("🤖 Proactive Assistant")
    st.markdown("Ask for weekly summaries, set reminders, or get help organizing your knowledge.")
    
    # Initialize chat history
    if "agent_messages" not in st.session_state:
        st.session_state.agent_messages = []
    
    # Display chat messages
    for message in st.session_state.agent_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Talk to the assistant..."):
        # Add user message to chat history
        st.session_state.agent_messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.agent_messages.append({"role": "assistant", "content": response})