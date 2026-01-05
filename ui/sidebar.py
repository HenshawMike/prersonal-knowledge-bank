import streamlit as st
import os
from config.settings import settings

def render():
    with st.sidebar:
        st.header("📤 Upload Knowledge")
        st.markdown("Add notes, PDFs, research papers, ideas — anything!")
        
        uploaded = st.file_uploader(
            "Drop files here",
            accept_multiple_files=True,
            type=['pdf', 'txt', 'md', 'docx', 'csv', 'html']
        )
        
        if uploaded:
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
            new_count = 0
            for file in uploaded:
                path = os.path.join(settings.UPLOAD_DIR, file.name)
                if not os.path.exists(path):
                    with open(path, "wb") as f:
                        f.write(file.getbuffer())
                    new_count += 1
            if new_count:
                st.success(f"✅ {new_count} new file(s) added! Rebuilding index...")
                st.rerun()
            else:
                st.info("All files already uploaded.")
        
        st.markdown("---")
        st.caption("🔒 Private • Persistent •  Embeddings")