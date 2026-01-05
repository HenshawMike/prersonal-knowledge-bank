import streamlit as st
import os
import glob
from datetime import datetime
from config.settings import settings


def render(index):
    st.header("📊 Knowledge Dashboard")

    files= glob.glob(os.path.join(settings.UPLOAD_DIR, "*.*"))
    num_files = len(files)
    num_chunks = len(index.docstore.docs) if index else 0

    st.markdown("---")
    
    if files:
        st.subheader("📄 Recent Uploads")
        recent = sorted(files, key=os.path.getmtime, reverse=True)[:10]
        for path in recent:
            name = os.path.basename(path)
            time = datetime.fromtimestamp(os.path.getmtime(path))
            with st.expander(f"📄 {name}"):
                st.caption(f"Added: {time.strftime('%b %d, %Y • %H:%M')}")
    else:
        st.info("No knowledge yet — upload files in the sidebar!")
    
    st.markdown("---")
    st.subheader("🔮 Future Agents")
    cols = st.columns(3)
    cols[0].info("**Weekly Digest** – Auto-summary")
    cols[1].info("**Smart Reminders** – From your notes")
    cols[2].info("**Draft Assistant** – Write from knowledge")