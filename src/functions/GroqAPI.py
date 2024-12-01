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
            base_url="https://api.groq.com/openai/v1", api_key=api_key
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

    def single_completion(self, model, messages):
        # Logger at start
        _NAME = "single_completion"
        logging.debug(f"[{_NAME}] Start")
        logging.debug(f"[{_NAME}] 使用モデル: {model}")
        logging.debug(
            f"""
            [{_NAME}] リクエスト・メッセージ: {
                json.dumps(messages, indent=2, ensure_ascii=False)
            }
            """
        )

        try:
            # response = self.client.invoke(
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
            )
            assistant_completion = response.choices[0].message.content

            logging.debug(
                f"""
                [{_NAME}] レスポンスボディ: {
                    json.dumps(response.json(), indent=2, ensure_ascii=False)
                }
                """
            )
            assistant_completion = response.choices[0].message.content
        except Exception as ex:
            logging.error(f"[{_NAME}] エラー発生: {str(ex)}")
            assistant_completion = f"問い合わせに失敗しました（{ex}）"
        finally:
            logging.debug(f"[{_NAME}] 回答: {assistant_completion}")
            logging.debug(f"[{_NAME}] End..")

            return assistant_completion
