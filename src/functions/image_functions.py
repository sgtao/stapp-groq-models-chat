# image_functions.py
import base64
import io
from PIL import Image  # 追加


def process_image(image_data, target_height=320):
    """画像データを処理して指定された高さにリサイズする関数"""
    # バイトデータかファイルアップローダーの返り値かを判定
    if isinstance(image_data, bytes):
        image = Image.open(io.BytesIO(image_data))
    else:
        image = Image.open(image_data)

    # 現在のアスペクト比を維持しながら、目標の高さにリサイズ
    aspect_ratio = image.width / image.height
    new_width = int(target_height * aspect_ratio)
    resized_image = image.resize((new_width, target_height))

    # リサイズした画像をバイトデータに変換
    output = io.BytesIO()
    resized_image.save(output, format="PNG")
    return output.getvalue()


def encode_image_to_base64(image_bytes):
    """画像データをbase64エンコードする関数"""
    return base64.b64encode(image_bytes).decode("utf-8")
