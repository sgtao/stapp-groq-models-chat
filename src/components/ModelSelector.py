# ModelSelector.py
import streamlit as st

from functions.GroqAPI import GroqAPI


def _on_model_change():
    st.session_state.selected_model = st.session_state.model_selector


class ModelSelector:
    """Class for selecting the Groq model"""

    def __init__(self, filter=None):
        """Define the available models"""
        if "model_type" not in st.session_state:
            st.session_state.model_type = filter
        if "models" not in st.session_state:
            st.session_state.models = []
        if "selected_model" not in st.session_state:
            st.session_state.selected_model = None

        # モデル情報の取得（初回のみ）
        if (
            len(st.session_state.models) == 0
            or st.session_state.model_type != filter
        ):
            st.session_state.selected_model = None
            st.session_state.models = []
            self.initialize_options(filter)

    def initialize_options(self, filter):
        # クライアントの初期化
        client = GroqAPI(st.session_state.groq_api_key)
        models = client.get_models_info()
        sorted_models = client.sort_models(
            data=models,
            supplement_filter=filter,
        )
        model_ids = [model["id"] for model in sorted_models]
        st.session_state.models = model_ids

    def select_box(self):
        """
        Display the model selection form in the sidebar
        Returns:
            st.selectbox of Models
        """

        selected_model = st.selectbox(
            "Select Model (モデルを選択):",
            st.session_state.models,
            key="model_selector",
            on_change=_on_model_change,
            index=(
                st.session_state.models.index(st.session_state.selected_model)
                if st.session_state.selected_model
                else 0
            ),
        )
        st.session_state.selected_model = selected_model
        return selected_model
