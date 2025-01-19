# 03_image_description.py.py
import io
import time

import streamlit as st
from streamlit_paste_button import paste_image_button

from components.GropApiKey import GropApiKey
from components.ModelSelector import ModelSelector

# from components.MessageController import MessageController
from components.ModelParameters import ModelParameters

# from components.FileUploaders import FileUploaders
# from components.Messages import Messages
from components.ModalDialogs import ModalDialogs

from functions.GroqAPI import GroqAPI
from functions.image_functions import process_image
from functions.image_functions import encode_image_to_base64


# ページ設定に移動
st.set_page_config(
    page_title="Groq Image Description", layout="wide", page_icon="🏞"
)

_DEFAULT_IMAGE_PROMPT = "画像を解説してください"


def init_session_state(optype=None):
    initial_states = {
        "clear_state": False,
        "image_type": None,
        "image_data": None,
        "image_prompt": _DEFAULT_IMAGE_PROMPT,
        "image_message": [],
        "file_image": None,
        "pasted_image": None,
        "image_response": [],
        "messages": [],
    }
    for key, value in initial_states.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_image_prompt():
    """
    image_prompt 入力をReset
    """
    st.session_state.text_input_image_prompt = _DEFAULT_IMAGE_PROMPT
    st.session_state.image_prompt = _DEFAULT_IMAGE_PROMPT


def main():
    # 初期化を最初に行う
    groq_api_key = GropApiKey()

    # サイドバー：APIキー入力
    groq_api_key.input_key()

    # メイン画面の構築
    st.page_link("main.py", label="Go to Main", icon="🏠")
    st.subheader(
        "🏞 Groq-API Image Description (画像説明)",
        divider="blue",
    )
    if groq_api_key.has_key() is False:
        st.warning("Input Groq API-Key at sidebar")
        return

    # チャットクライアントの初期化
    client = GroqAPI(st.session_state.groq_api_key)

    model_selector = ModelSelector("Vision-Enhanced")
    model_params = ModelParameters()
    # file_uploaders = FileUploaders()
    # messages = Messages()
    # message_controller = MessageController()
    modal_dialogs = ModalDialogs()

    # セッション状態の初期化
    init_session_state()

    # クリア状態のチェックと処理
    if st.session_state.clear_state:
        st.session_state.image_type = None
        st.session_state.file_image = None
        st.session_state.pasted_image = None
        st.session_state.image_message = []
        st.session_state.image_response = []
        # if "image_uploader" in st.session_state:
        #     st.session_state.image_uploader = None
        if "paste_button" in st.session_state:
            st.session_state.paste_button = None
        st.session_state.clear_state = False  # リセット

    # サイドバーの設定
    with st.sidebar:
        # パラメータ設定UIの表示
        st.write("Setup LLM Prameters:")
        model_selector.select_box()
        model_params.render_tuning_parameters()
        model_params.render_sysprompt_editor()
        modal_dialogs.render_parameter_store_loader()

    # メイン領域のレイアウト構築
    left, right = st.columns([0.4, 0.6], gap="small", border=True)
    with left:
        st.write("#### 画像処理 :")
        # ユーザー入力
        prompt = st.text_input(
            label="#### Prompt :",
            value=st.session_state.image_prompt,
            key="text_input_image_prompt",
        )
        # print(prompt)
        st.session_state.image_prompt = prompt
        if st.button(
            "Reset Prompt",
            type="secondary",
            on_click=reset_image_prompt,
        ):
            st.success("Reset Prompt.")
            time.sleep(1)
            st.rerun()
        st.write("##### Image :")
        with st.expander(label="set image", expanded=False):
            paste_result = paste_image_button(
                label="📋 Paste Image data",
                text_color="#ffffff",
                background_color="#3498db",
                hover_background_color="#2980b9",
                key="paste_button",
            )
            if paste_result.image_data is not None:
                # st.write(paste_result)
                # PIL.Image を bytes に変換
                img_byte_arr = io.BytesIO()
                paste_result.image_data.save(img_byte_arr, format="PNG")
                st.session_state.pasted_image = img_byte_arr.getvalue()
                st.session_state.image_type = "pasted_image"

            uploaded_file = st.file_uploader(
                label="📂 Upload Image File",
                type=["png", "jpg", "jpeg"],
                key="image_uploader",
            )
            if uploaded_file is not None:
                # ファイルを読み込んでバイトデータに変換
                st.session_state.image_type = "file_image"
                st.session_state.file_image = uploaded_file.getvalue()
                st.info("At File, Click 'x' after load.")

        # 画像データの表示
        if st.session_state.image_type is None:
            st.info("Upload file or paste image")
        else:
            resized_image = None
            if st.button("Clear Image", type="secondary"):
                st.success("Clear Image data.")
                st.session_state.clear_state = True
                time.sleep(1)
                st.rerun()

            # 画像をリサイズして表示
            try:
                if st.session_state.image_type == "file_image":
                    resized_image = process_image(st.session_state.file_image)
                else:
                    resized_image = process_image(
                        st.session_state.pasted_image
                    )
            except Exception as e:
                st.error(f"During show image, error occurred!: {str(e)}")
            st.image(resized_image)
            st.session_state.image_data = resized_image

    with right:
        st.write("#### 認識処理 :")
        # アシスタントの応答
        if st.button(
            label="Recognize Image",
            icon="🤔",
            type="primary",
            disabled=(st.session_state.image_type is None),
        ):
            # 画像をbase64エンコードしてユーザーメッセージを付与する
            image_bytes = st.session_state.image_data
            base64_image = encode_image_to_base64(image_bytes)
            image_url = f"data:image/jpeg;base64,{base64_image}"

            # 毎回、メッセージ初期化を行いプロンプトを準備
            st.session_state.image_message = []
            st.session_state.image_response = []
            if st.session_state.use_sys_prompt:
                prompt += f"\n{st.session_state.system_prompt}\n"
            st.session_state.image_message.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url},
                        },
                    ],
                }
            )

            with st.chat_message("assistant"):
                with st.spinner("考え中..."):
                    assistant_response = client.single_completion(
                        model=st.session_state.selected_model,
                        messages=st.session_state.image_message,
                        llm_params=st.session_state.llm_params,
                    )
                    st.markdown(assistant_response)

                    st.session_state.image_response.append(
                        {
                            "role": "assistant",
                            "content": assistant_response,
                        }
                    )
                    # st.rerun()


if __name__ == "__main__":
    main()
