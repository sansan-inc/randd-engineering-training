from typing import Protocol


class IPreprocessor(Protocol):
    """テキストを前処理するためのインターフェース"""

    def __call__(self, text: str) -> str:
        """
        前処理を実行するメソッド.
        関数も許容するために`__call__`メソッドにしている.

        Args:
            text: 前処理したいテキスト

        Returns:
            前処理済みテキスト
        """
        ...
