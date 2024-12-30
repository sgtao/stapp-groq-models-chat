# 12_groq_chatbot.py
import streamlit as st

from components.GropApiKey import GropApiKey
from components.ModelSelector import ModelSelector
from components.MessageController import MessageController
from components.ModelParameters import ModelParameters

from functions.GroqAPI import GroqAPI

# ページ設定に移動
st.set_page_config(page_title="Groq ChatBot", layout="wide", page_icon="💭")


def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main():
    # 初期化を最初に行う
    init_chat_history()
    message_controller = MessageController()
    groq_api_key = GropApiKey()
    model_selector = ModelSelector("Base-Language")
    model_params = ModelParameters()

    # サイドバー：APIキー入力
    groq_api_key.input_key()

    # チャットクライアントの初期化
    client = GroqAPI(st.session_state.groq_api_key)

    # メイン画面の構築
    st.page_link("main.py", label="Go to Main", icon="🏠")
    st.subheader(
        "💭 Groq-API ChatBot (Groq チャットボット)",
        divider="blue",
    )
    if groq_api_key.has_key() is False:
        st.warning("Input Groq API-Key at sidebar")
        return

    # 会話履歴の保存・削除
    if len(st.session_state.messages) <= 0:
        st.write(
            "Setup Model and parameters:モデルとパラメータを設定してください"
        )
        model_selector.select_box()
        # パラメータ設定UIの表示
        model_params.render_tuning_parameters()
    else:
        # チャット履歴の初期化と表示
        display_chat_history()
        message_controller.place_components(st.session_state.messages)

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
                    llm_params=st.session_state.llm_params,
                )
                st.markdown(assistant_response)

                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_response}
                )

                st.rerun()


if __name__ == "__main__":
    main()
