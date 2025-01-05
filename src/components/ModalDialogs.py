# ModalDialogs.py
from datetime import datetime
import time
import yaml

import streamlit as st

from components.ModelParameters import ModelParameters


class ModalDialogs:

    def __init__(self) -> None:
        self.model_parameters = ModelParameters()
        self._initialize_session_state()

    def _initialize_session_state(self) -> None:
        pass

    @st.dialog("Setting Info.")
    def modal(self, type):
        st.write(f"Modal for {type}:")
        if type == "session-state":
            self.show_parameters()
            self._modal_closer()
        elif type == "save-parameters":
            self.save_parameters()
            self._modal_closer()
        elif type == "load-parameters":
            self.load_parameters()
            self._modal_closer()
        else:
            st.write("No Definition.")
            self._modal_closer()

    def _modal_closer(self):
        if st.button(label="Close Modal"):
            st.info("モーダルを閉じます...")
            time.sleep(1)
            st.rerun()

    # 『表示』モーダル：
    def show_parameters(self):
        # セッション状態の全内容を表示
        with st.expander(
            "#### session_state状態（for debug）", expanded=False
        ):
            st.json(st.session_state)  # JSON形式で表示

    # 『保存』モーダル：
    def save_parameters(self):
        with st.expander("Save Parameters ?", expanded=False):
            pad = "stappModelParameters.yaml"
            # セッション状態からパラメータを取得
            model_params = {
                "selected_model": st.session_state.selected_model,
                "llm_params": self.model_parameters.get_llm_params(),
                "use_sys_prompt": st.session_state.use_sys_prompt,
                "system_prompt": st.session_state.system_prompt,
            }

            # YAMLに変換
            yaml_str = yaml.dump(
                model_params, allow_unicode=True, default_flow_style=False
            )

            # ダウンロードボタンを表示
            st.download_button(
                label="Download as YAML",
                data=yaml_str,
                file_name=f"{datetime.now().strftime('%Y%m%d-%H%M%S')}_{pad}",
                mime="text/yaml",
            )

    # 『読み込み』モーダル：
    def load_parameters(self):
        uploaded_file = st.file_uploader(
            "YAMLファイルをアップロード", type=["yaml", "yml"]
        )

        if uploaded_file is not None:
            try:
                # YAMLファイルを読み込み
                yaml_content = yaml.safe_load(uploaded_file)
                # st.json(yaml_content)

                # セッション状態を更新
                st.session_state.selected_model = yaml_content[
                    "selected_model"
                ]
                self.model_parameters.set_llm_params(
                    yaml_content["llm_params"]
                )
                st.session_state.use_sys_prompt = yaml_content[
                    "use_sys_prompt"
                ]
                st.session_state.system_prompt = yaml_content["system_prompt"]

                st.success("パラメータを正常に読み込みました")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"パラメータの読み込みに失敗しました: {str(e)}")

    def render_parameter_store_loader(self) -> None:
        st.write("##### Setting Info.")
        (
            col1,
            col2,
            col3,
            col4,
            col5,
        ) = st.columns(5)
        with col1:
            if st.button(help="Show Session State", label="📟"):
                self.modal("session-state")
        with col2:
            if st.button(help="Save Params.", label="📥"):
                self.modal("save-parameters")
        with col3:
            if st.button(help="Load Params.", label="📤"):
                self.modal("load-parameters")
        with col4:
            pass
        with col5:
            pass
