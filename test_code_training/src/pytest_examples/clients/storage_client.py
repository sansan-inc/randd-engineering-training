import os


class StorageClient:
    """
    以下のようなクラスを想定してのデモクラス
    - GCPのCloudStorageにアクセスするためのクラス
    - AWSのS3にアクセスするためのクラス
    このクラスのメソッドを実行するためには何かしらの権限が必要になる(ことを想定)

    特定の条件下でインスタンス化でエラーが起きるクラスを用いるテストするときの対処法を説明するために作成したクラス
    """

    def __init__(self) -> None:
        # 権限がないことを環境変数で表現している
        if os.environ.get("HAS_STORAGE_AUTHORIZATION") != "true":
            raise PermissionError("Not authorized.")

    def get_text(self, document_id: str) -> str:
        return f"Sansan株式会社_{document_id}"  # ダミーのテキストを返す
