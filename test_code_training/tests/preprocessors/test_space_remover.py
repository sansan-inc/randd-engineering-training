from typing import NamedTuple

import pytest

from pytest_examples.preprocessors.space_remover import remove_space


def test_remove_space_no_parametrize() -> None:
    """
    `@pytest.mark.parametrize`を使用しないでテストを書いた例
    このテスト関数では, テストケースが独立して実行されないため, 1つ目のassert文が失敗してしまうと, 2つ目のassert文は比較されない.
    よって, テストの書き方は `test_remove_space_no_parametrize` より `test_remove_space` が好ましい
    """
    assert remove_space(text="San san") == "Sansan"
    assert remove_space(text="Yon yon") == "Yonyon"


@pytest.mark.parametrize(
    ("text", "expected_text"),
    [
        ("San san", "Sansan"),
        ("Yon yon", "Yonyon"),
    ],
)
def test_remove_space(text: str, expected_text: str) -> None:
    """
    Args:
        text: `remove_space`関数に入力するテキスト
        expected_text: `remove_space`関数の出力として期待するテキスト
    """
    assert remove_space(text=text) == expected_text


class RemoveSpaceTestCase(NamedTuple):
    text: str
    expected_text: str


@pytest.mark.parametrize(
    RemoveSpaceTestCase._fields,
    [
        RemoveSpaceTestCase(text="San san", expected_text="Sansan"),
        RemoveSpaceTestCase(text="Yon yon", expected_text="Yonyon"),
    ],
)
def test_remove_space_clean_test_case(text: str, expected_text: str) -> None:
    """
    テストケースが複雑になる場合は, 専用のNamedTupleで定義することで見やすくなります

    Args:
        text: `remove_space`関数に入力するテキスト
        expected_text: `remove_space`関数の出力として期待するテキスト
    """
    assert remove_space(text=text) == expected_text
