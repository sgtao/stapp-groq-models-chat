# 11_groq_models_info.py
import streamlit as st

from components.GropApiKey import GropApiKey
from functions.GroqAPI import GroqAPI

# # メインページに移動
# st.page_link("main.py", label="Go to Main", icon="🏠")
st.set_page_config(page_title="Groq モデル情報", layout="wide")


# def display_model_info(self, models: List[Dict]):
def display_model_info(models):
    st.header("利用可能なGroqモデル")

    for model in models:
        with st.expander(f"📚 {model['id']}", expanded=False):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**基本情報**")
                st.write(f"開発元: {model.get('owned_by', '不明')}")
                st.write(
                    f"コンテキストウィンドウ: {model.get('context_window', '不明')} tokens"
                )

            with col2:
                st.markdown("**モデルの特徴**")
                if "tool-use" in model["id"]:
                    st.write("✅ ツール/関数呼び出し対応")
                if "preview" in model["id"]:
                    st.write("🔬 プレビュー版")
                if "instant" in model["id"]:
                    st.write("⚡ 高速推論対応")

def main():
    # sidebar: apikey input
    groq_api_key = GropApiKey()
    groq_api_key.input_key()

    # main content
    st.title("Groq モデル情報ダッシュボード")
    if groq_api_key.has_key() == False:
        st.warning("Input Groq API-Key at sidebar")
        return

    try:
        client = GroqAPI(st.session_state.groq_api_key)
        models_info = client.get_models_info()
        display_model_info(models_info)

    except Exception as e:
        st.error(f"モデル情報の取得に失敗しました: {str(e)}")

if __name__ == "__main__":
    main()