import streamlit as st

st.set_page_config(
    page_title="Groq-API App",
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
    "pages/01_groq_models_info.py", label="Go to Models info. page", icon="📚"
)
st.page_link(
    "pages/02_groq_chatbot.py", label="Go to Groq Chatbot page", icon="💭"
)
st.page_link(
    "pages/03_image_description.py",
    label="Go to Image Description",
    icon="🏞",
)
