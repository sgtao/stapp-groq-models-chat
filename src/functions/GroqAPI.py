# GroqAPI.py
import json
import logging
import requests

import openai

_BASE_URL = "https://api.groq.com/openai/v1"
logging.basicConfig(level=logging.DEBUG)


class GroqAPI:
    """GroqAPI クラス：
    Groq APIとのインターフェースを提供します。
    このクラスは、Groq APIを使用して自然言語処理タスクを実行するための
    メソッドを提供します。

    Attributes:
        client (Groq): Groq APIクライアントインスタンス
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=_BASE_URL,
        )

    def get_models_info(self):
        """モデル情報を取得"""
        # Logger at start
        _NAME = "get_models_info"
        logging.debug(f"[{_NAME}] Start")
        url = _BASE_URL + "/models"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        logging.debug(f"[{_NAME}] GET Method to {url}")
        response = requests.get(url, headers=headers)
        # logging.debug(f"[{_NAME}] response is {response}")
        logging.debug(f"[{_NAME}] ステータスコード: {response.status_code}")
        response.raise_for_status()
        # logging.debug(
        #     f"""
        #     [{_NAME}] レスポンスヘッダー: {
        #         json.dumps(
        #             dict(response.headers),
        #             indent=2,
        #             ensure_ascii=False)
        #     }
        #     """
        # )
        logging.debug(
            f"""
            [{_NAME}] レスポンスボディ: {
                json.dumps(response.json(), indent=2, ensure_ascii=False)
            }
            """
        )

        data = response.json()["data"]
        logging.debug(f"[{_NAME}] 取得したモデル数: {len(data)}")

        logging.debug(f"[{_NAME}] End..")

        return data
