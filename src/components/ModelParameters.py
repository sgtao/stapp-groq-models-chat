# ModelParameters.py
import streamlit as st
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class LLMParameters:
    temperature: float = 0.7
    top_p: float = 1.0
    max_tokens: int = 512
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
        }


_DEFAULT_SYS_PROMPT: str = (
    """あなたは聡明なAIです。ユーザの入力に全て日本語で返答を生成してください"""
)


@dataclass
class SystemPrompt:
    use_prompt: bool = True
    prompt: str = _DEFAULT_SYS_PROMPT
    disabled_edit: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "use_prompt": self.use_prompt,
            "prompt": self.prompt,
            "disabled_edit": self.disabled_edit,
        }


class ModelParameters:

    def __init__(self) -> None:
        self._initialize_session_state()

    def _initialize_session_state(self) -> None:
        if "system_prompt" not in st.session_state:
            st.session_state.use_sys_prompt = True
            st.session_state.system_prompt = _DEFAULT_SYS_PROMPT
            st.session_state.fixed_sys_prompt = False
            # system_prompt = {
            #     "use_prompt": True,
            #     "prompt": _DEFAULT_SYS_PROMPT,
            #     "disabled_edit": True,
            # }
            # st.session_state.system_prompt = system_prompt
            # st.session_state.system_prompt = SystemPrompt()

        if "llm_params" not in st.session_state:
            st.session_state.llm_params = LLMParameters()

    def render_tuning_parameters(self) -> None:
        with st.expander("Set Parameters (パラメタ設定):", expanded=False):
            new_temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.llm_params.temperature,
                step=0.1,
                help="出力のランダム性を制御（0-2）",
            )
            new_top_p = st.slider(
                "Top P",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.llm_params.top_p,
                step=0.1,
                help="確率質量の上位を考慮",
            )
            new_max_tokens = st.slider(
                "Max Tokens",
                min_value=1000,
                max_value=8000,
                value=st.session_state.llm_params.max_tokens,
                step=1000,
                help="生成する最大トークン数",
            )
            new_frequency_penalty = st.slider(
                "Frequency Penalty",
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.llm_params.frequency_penalty,
                step=0.1,
                help="単語の繰り返しにペナルティを与える",
            )
            new_presence_penalty = st.slider(
                "Presence Penalty",
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.llm_params.presence_penalty,
                step=0.1,
                help="トークンの重複を抑制",
            )

            # パラメータの更新
            if self._check_params_changed(
                new_temperature,
                new_max_tokens,
                new_frequency_penalty,
                new_presence_penalty,
                new_top_p,
            ):
                st.session_state.llm_params = LLMParameters(
                    temperature=new_temperature,
                    max_tokens=new_max_tokens,
                    frequency_penalty=new_frequency_penalty,
                    presence_penalty=new_presence_penalty,
                    top_p=new_top_p,
                )
                st.success(
                    f"パラメータを更新しました:\n{st.session_state.llm_params}"
                )

    def _check_params_changed(
        self, temp, max_tok, freq_pen, pres_pen, top_p
    ) -> bool:
        current = st.session_state.llm_params
        return (
            temp != current.temperature
            or max_tok != current.max_tokens
            or freq_pen != current.frequency_penalty
            or pres_pen != current.presence_penalty
            or top_p != current.top_p
        )

    def get_llm_params(self) -> Dict[str, Any]:
        return st.session_state.llm_params.to_dict()
