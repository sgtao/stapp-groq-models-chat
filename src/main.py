import streamlit as st

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

"""
# Welcome to Streamlit!

This Application has some pages using Groq-API LLM.
"""

# サイドバーのページに移動
st.page_link(
    "pages/11_groq_models_info.py", label="Go to Models info. page", icon="📚"
)
st.page_link(
    "pages/12_groq_chatbot.py", label="Go to Groq Chatbot page", icon="💭"
)
