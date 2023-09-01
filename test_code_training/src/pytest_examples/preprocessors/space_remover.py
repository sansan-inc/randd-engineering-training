import re


def remove_space(text: str) -> str:
    """
    空白を除去する関数

    Args:
        text: 空白を除去したいテキスト

    Returns:
        空白を除去されたテキスト
    """
    return re.sub(r"\s", "", text)
