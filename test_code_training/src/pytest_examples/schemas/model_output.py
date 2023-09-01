from pydantic import BaseModel, Field


class ModelOutput(BaseModel):
    """モデルが出力するテキスト抽出結果を格納するデータクラス"""

    text_length: int = Field(ge=0, title="テキスト長")
    start_position: int = Field(ge=0, title="テキストから抽出する開始位置")
    end_position: int = Field(ge=0, title="テキストから抽出する終了位置")
