# 12_groq_chatbot.py
import time

import streamlit as st

from components.GropApiKey import GropApiKey
from components.ModelSelector import ModelSelector

from functions.GroqAPI import GroqAPI


def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main():
    st.header("Groq チャットボット")
    # 初期化を最初に行う
    init_chat_history()

    # サイドバー：APIキー入力
    groq_api_key = GropApiKey()
    groq_api_key.input_key()

    if groq_api_key.has_key() is False:
        st.warning("Input Groq API-Key at sidebar")
        return

    # チャットクライアントの初期化
    client = GroqAPI(st.session_state.groq_api_key)

    # モデル選択
    with st.sidebar:
        model_selector = ModelSelector()
        model_selector.select_box()

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
                    model=st.session_state.selected_model,
                    messages=st.session_state.messages,
                )
                st.markdown(assistant_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_response}
        )

    # 会話履歴の保存・削除
    if len(st.session_state.messages) > 0:
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.info("会話履歴をクリアしました")
            time.sleep(3)
            st.rerun()


if __name__ == "__main__":
    main()
