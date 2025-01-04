# 12_groq_chatbot.py
import streamlit as st

from components.GropApiKey import GropApiKey
from components.ModelSelector import ModelSelector
from components.MessageController import MessageController
from components.ModelParameters import ModelParameters
from components.FileUploaders import FileUploaders

from functions.GroqAPI import GroqAPI


# ページ設定に移動
st.set_page_config(page_title="Groq ChatBot", layout="wide", page_icon="💭")


def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_chat_history():
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main():
    # 初期化を最初に行う
    init_chat_history()
    message_controller = MessageController()
    groq_api_key = GropApiKey()
    model_selector = ModelSelector("Base-Language")
    model_params = ModelParameters()
    file_uploaders = FileUploaders()

    # サイドバー：APIキー入力
    groq_api_key.input_key()

    # チャットクライアントの初期化
    client = GroqAPI(st.session_state.groq_api_key)

    with st.sidebar:
        # パラメータ設定UIの表示
        st.write("Setup LLM Prameters:")
        model_selector.select_box()
        model_params.render_tuning_parameters()
        model_params.render_sysprompt_editor()

    # メイン画面の構築
    st.page_link("main.py", label="Go to Main", icon="🏠")
    st.subheader(
        "💭 Groq-API ChatBot (Groq チャットボット)",
        divider="blue",
    )
    if groq_api_key.has_key() is False:
        st.warning("Input Groq API-Key at sidebar")
        return

    # セッション状態の全内容を表示
    # with st.expander("#### session_state状態（for debug）", expanded=False):
    #     st.json(st.session_state)  # JSON形式で表示

    if len(st.session_state.messages) > 0:
        # チャット履歴の初期化と表示
        display_chat_history()
        message_controller.place_components(st.session_state.messages)

    # 会話履歴の保存・削除
    st.subheader("Attachment text file or chat history json:")
    col1, col2 = st.columns([1, 1])
    updated_file_content = None
    # ファイルアップロード機能
    with col1:
        # uploaded_file = file_uploaders.text_file_upload(message)
        updated_file_content = file_uploaders.text_file_upload()
    # chat_history アップロード機能
    with col2:
        # upload_file = file_uploaders.json_chat_history(message)
        file_uploaders.json_chat_history()

    # アップロードファイルは手動クリアとなるため、メッセージ表示
    # if uploaded_file is not None:
    #     st.warning("After clear chat, CLEAR upload_file manualy.")

    # ユーザー入力
    if prompt := st.chat_input("メッセージを入力してください:"):
        # 最初のメッセージは`system_prompt`を付与する
        if (
            len(st.session_state.messages) == 0
            and st.session_state.use_sys_prompt
        ):
            st.session_state.messages.append(
                {
                    "role": "system",
                    "content": st.session_state.system_prompt,
                }
            )

        if updated_file_content is not None:
            st.session_state.messages.append(
                {"role": "system", "content": updated_file_content}
            )

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
