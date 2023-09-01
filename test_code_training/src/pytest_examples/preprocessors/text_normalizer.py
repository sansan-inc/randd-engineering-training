import unicodedata


class TextNormalizer:
    def __call__(self, text: str) -> str:
        """
        Unicode正規化をするメソッド

        Args:
            text: Unicode正規化をしたいテキスト

        Returns:
            Unicode正規化済みのテキスト
        """
        return unicodedata.normalize("NFKC", text)
