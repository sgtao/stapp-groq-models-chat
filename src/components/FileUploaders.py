# FileUploaders.py
import json
import time

# from io import StringIO
import chardet
import streamlit as st


class FileUploaders:
    def __init__(self):
        self._initialize_session_state()

    def _initialize_session_state(self) -> None:
        # pass
        if "last_attach_filename" not in st.session_state:
            st.session_state.last_attach_filename = ""

    def _session_state_has_messages(self):
        if len(st.session_state.messages) > 0:
            return True
        else:
            return False

    def _session_state_has_attach_file(self):
        if "last_attach_filename" in st.session_state:
            return True
        else:
            return False

    def _is_new_attach_file(self, filename):
        if st.session_state.last_attach_filename != filename:
            return True
        else:
            return False

    def _read_and_convert_to_utf8(self, uploaded_file):
        # # To convert to a string based IO:
        # stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # st.write(stringio)
        # return stringio
        content = uploaded_file.read()
        detected = chardet.detect(content)
        encoding = detected["encoding"]

        if encoding.lower() != "utf-8":
            try:
                content = (
                    content.decode(encoding).encode("utf-8").decode("utf-8")
                )
            except UnicodeDecodeError:
                st.error(
                    f"ファイルの文字コード（{encoding}）を正しく変換できませんでした。"
                )
                return None
        else:
            content = content.decode("utf-8")

        return content

    def text_file_upload(self):
        uploaded_file = st.file_uploader(
            "Upload an attachment file with a chat.",
            type=("txt", "md"),
        )
        if uploaded_file is not None:
            # st.write(uploaded_file)
            st.info("When clear file, Click 'x' manualy.")
            # ファイルの内容を読み取り、UTF-8に変換する
            file_content = self._read_and_convert_to_utf8(uploaded_file)
            if file_content is not None:

                if self._is_new_attach_file(uploaded_file.name):
                    st.session_state.last_attach_filename = uploaded_file.name

                attach_file = f"""
                # {uploaded_file.name}
                -----
                {file_content}
                """

                return attach_file

            else:
                st.error("ファイルの内容を正しく読み取れませんでした。")

        return None

    def json_chat_history(self):
        uploaded_file = st.file_uploader(
            "Before 1st chat, upload previous chat history",
            type=("json"),
            disabled=self._session_state_has_messages(),
        )
        if (
            self._session_state_has_messages() is False
            and uploaded_file is not None
        ):
            st.info("After load, Click 'x' manualy.")
            # message.アップロードされたファイルは手動でクリア
            chat_history_messages = json.load(uploaded_file)
            st.session_state.messages = []
            for message in chat_history_messages:
                st.session_state.messages.append(message)
            st.info("会話履歴を更新します...")
            time.sleep(3)
            st.rerun()
