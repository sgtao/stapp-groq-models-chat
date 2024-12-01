# 12_groq_chatbot.py
import streamlit as st

from components.GropApiKey import GropApiKey
from functions.GroqAPI import GroqAPI


def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main():
    st.title("Groq チャットボット")

    # サイドバー：APIキー入力
    groq_api_key = GropApiKey()
    groq_api_key.input_key()

    if "groq_api_key" not in st.session_state:
        st.warning("APIキーを入力してください")
        return

    # チャットクライアントの初期化
    client = GroqAPI(st.session_state.groq_api_key)

    # モデル選択
    models = client.get_models_info()
    model_ids = [model["id"] for model in models]
    selected_model = st.selectbox("モデルを選択:", model_ids)

    # チャット履歴の初期化と表示
    init_chat_history()
    display_chat_history()

    # ユーザー入力
    if prompt := st.chat_input("メッセージを入力してください:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # アシスタントの応答
        with st.chat_message("assistant"):
            with st.spinner("考え中..."):
                assistant_response = client.single_completion(
                    model=selected_model,
                    messages=st.session_state.messages,
                )
                st.markdown(assistant_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_response}
        )


if __name__ == "__main__":
    main()
