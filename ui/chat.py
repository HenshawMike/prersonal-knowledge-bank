import streamlit as  st
import core.retriever as chat_engine

def render(chat_engine):
    st.header("💬 Chat with Your Second Brain")

    if "messages" not in  st.session_state:
        st.session_state.messages =[]
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if  prompt := st.chat_input ("Ask anything from your knowledge..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if chat_engine:
            with st.chat_message("assistant"):
                with  st.spinner("Searching your knowledge..."):
                    response = chat_engine.chat(prompt)
                    st.markdown(response.response)
                    st.session_state.messages.append({"role": "assistant" , "content": response.response})
        else:
            st.warning("Upload some files first to build your knowledge base!")