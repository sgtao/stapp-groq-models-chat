# 12_groq_chatbot.py
import streamlit as st

from components.GropApiKey import GropApiKey

# from components.ModelSelector import ModelSelector
from functions.GroqAPI import GroqAPI


def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def init_model_state():
    if "models" not in st.session_state:
        st.session_state.models = []
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = None


def on_model_change():
    st.session_state.selected_model = st.session_state.model_selector


def main():
    st.title("Groq チャットボット")
    # 初期化を最初に行う
    init_chat_history()
    init_model_state()

    # サイドバー：APIキー入力
    groq_api_key = GropApiKey()
    groq_api_key.input_key()

    if "groq_api_key" not in st.session_state:
        st.warning("APIキーを入力してください")
        return

    # チャットクライアントの初期化
    client = GroqAPI(st.session_state.groq_api_key)

    # モデル選択
    # モデル情報の取得（初回のみ）
    if len(st.session_state.models) == 0:
        models = client.get_models_info()
        model_ids = [model["id"] for model in models]
        st.session_state.models = model_ids

    selected_model = st.selectbox(
        "モデルを選択:",
        st.session_state.models,
        key="model_selector",
        on_change=on_model_change,
        index=(
            st.session_state.models.index(st.session_state.selected_model)
            if st.session_state.selected_model
            else 0
        ),
    )
    st.session_state.selected_model = selected_model

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


if __name__ == "__main__":
    main()
