# ModalDialogs.py
import streamlit as st


@st.dialog("Setting Info.")
def modal(type):
    st.write(f"Modal for {type}:")
    if type == "session-state":
        # セッション状態の全内容を表示
        with st.expander(
            "#### session_state状態（for debug）", expanded=False
        ):
            st.json(st.session_state)  # JSON形式で表示
        _modal_closer()
    else:
        st.write("No Definition.")
        _modal_closer()


def _modal_closer():
    if st.button(label="Close"):
        st.rerun()


class ModalDialogs:

    def __init__(self) -> None:
        self._initialize_session_state()

    def _initialize_session_state(self) -> None:
        pass

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
                modal("session-state")
        with col2:
            if st.button(help="Save Params.", label="📥"):
                pass
        with col3:
            if st.button(help="Load Params.", label="📤"):
                pass
        with col4:
            pass
        with col5:
            pass
