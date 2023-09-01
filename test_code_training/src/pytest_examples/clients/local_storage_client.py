from pathlib import Path


class LocalStorageClient:
    """ローカルのディレクトリ上にあるデータのためのクライアント"""

    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path

    def get_text(self, document_id: str) -> str:
        return self.root_path.joinpath(f"{document_id}.txt").read_text()
