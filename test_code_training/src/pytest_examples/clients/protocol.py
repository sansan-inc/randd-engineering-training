from typing import Protocol


class IClient(Protocol):
    """データを取得するためのクライアントのインターフェース"""

    def get_text(self, document_id: str) -> str:
        """
        文書IDに紐づくテキストを取得するためのメソッド

        Args:
            document_id: 文書ID

        Returns:
            テキスト
        """
        ...
