# MessageController.py
from datetime import datetime
import json
import time

import streamlit as st


class MessageController:
    def __init__(self):
        self.api_key = ""
        # API-KEYのプリセット確認
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # self.place_components(st.session_state.message)

    # 『クリア』ボタン：
    def clear_button(self):
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.info("会話履歴をクリアします...")
            time.sleep(3)
            st.rerun()

    # 『再試行』（削除）ボタン：
    def delete_last_message(self):
        # if st.button("Delete Last Message"):
        if st.button("Retry Chat"):
            if len(st.session_state.messages) > 0:
                # 最後のメッセージが"assistant"ならば２つ削除
                popped_msg = st.session_state.messages.pop()
                if popped_msg["role"] == "assistant":
                    st.session_state.messages.pop()

                st.info("最後のメッセージを削除しました")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("削除できるメッセージがありません")

    # 『保存』ボタン：
    def save_messages(self, messages):
        # チャット履歴をダウンロードするボタン
        with st.expander("Save chat ?", expanded=False):
            st.write("maybe need to DL twice...")
            # 現在の日時を取得してファイル名を生成
            # current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
            # filename = f"{current_time}_{message.get_name()}.json"
            pad = "stappChatHistory.json"
            # チャット履歴をJSONに変換
            chat_history = st.session_state.messages
            chat_json = json.dumps(chat_history, ensure_ascii=False, indent=2)
            st.download_button(
                label="Download as json",
                data=chat_json,
                # file_name=filename,
                file_name=f"{datetime.now().strftime('%Y%m%d-%H%M%S')}_{pad}",
                mime="application/json",
            )

    def place_components(self, messages):
        # カラムを作成
        col1, col2, col3 = st.columns([1, 1, 2])

        # 会話履歴クリアボタン
        with col1:
            self.clear_button()
        with col2:
            self.delete_last_message()

        # 会話履歴保存ボタン
        with col3:
            self.save_messages(messages)
