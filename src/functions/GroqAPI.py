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

    def _add_supplement_property(self, data):
        # append supplement
        for item in data:
            if "whisper" in item["id"]:
                item["supplement"] = "Voice-to-Text"
            elif "vision" in item["id"]:
                item["supplement"] = "Vision-Enhanced"
            elif "tool-use" in item["id"]:
                item["supplement"] = "Tool-Enhanced"
            else:
                item["supplement"] = "Base-Language"

        return data

    def sort_models(self, data, supplement_filter=None):
        """モデル情報をソートしフィルタリングする

        Args:
            data (list): モデル情報のリスト
            supplement_filter (str, optional): フィルタリングする supplement の値
                "Voice-to-Text", "Vision-Enhanced", "Base-Language" のいずれか

        Returns:
            list: ソート・フィルタリングされたモデル情報のリスト
        """
        # フィルタリング
        if supplement_filter:
            filtered_data = [
                item
                for item in data
                if item.get("supplement") == supplement_filter
            ]
        else:
            filtered_data = data

        # owned_by と id でソート
        sorted_data = sorted(
            filtered_data,
            key=lambda x: (
                x.get("supplement", ""),
                x.get("owned_by", ""),
                x.get("id", ""),
            ),
        )

        return sorted_data

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
        # logging.debug(
        #     f"""
        #     [{_NAME}] レスポンスボディ: {
        #         json.dumps(response.json(), indent=2, ensure_ascii=False)
        #     }
        #     """
        # )

        data = response.json()["data"]
        data_with_supplement = self._add_supplement_property(data)
        logging.debug(f"[{_NAME}] 取得したモデル数: {len(data)}")
        logging.debug(
            f"""
            [{_NAME}] レスポンスボディ: {
                json.dumps(data_with_supplement, indent=2, ensure_ascii=False)
            }
            """
        )
        logging.debug(f"[{_NAME}] End..")

        return data_with_supplement

    def single_completion(self, model, messages, llm_params=None):
        """
        単一の完了リクエストを実行します。

        Args:
            model (str): 使用するモデル名
            messages (list): メッセージのリスト
            llm_params (dict, optional): 生成パラメータの辞書
        """
        _NAME = "single_completion"
        logging.debug(f"[{_NAME}] Start")
        logging.debug(f"[{_NAME}] 使用モデル: {model}")
        if llm_params:
            logging.debug(f"""[{_NAME}] 生成パラメータ: {llm_params}""")

        logging.debug(
            f"""[{_NAME}] リクエスト・メッセージ: {
                json.dumps(messages, indent=2, ensure_ascii=False)
            }"""
        )

        try:
            response = None

            # LLMパラメータが指定されている場合は利用する
            if llm_params:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=llm_params.temperature,
                    top_p=llm_params.top_p,
                    max_tokens=llm_params.max_tokens,
                    frequency_penalty=llm_params.frequency_penalty,
                    presence_penalty=llm_params.presence_penalty,
                )
            else:
                # response = self.client.invoke(
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                )
            assistant_completion = response.choices[0].message.content

        except Exception as ex:
            logging.error(f"[{_NAME}] エラー発生: {str(ex)}")
            assistant_completion = f"問い合わせに失敗しました（{ex}）"

        finally:
            logging.debug(f"[{_NAME}] 回答: {assistant_completion}")
            logging.debug(f"[{_NAME}] End..")

            return assistant_completion
