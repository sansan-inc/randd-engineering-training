from typing import NamedTuple

import pytest

from pytest_examples.preprocessors.text_normalizer import TextNormalizer


class TextNormalizerTestCase(NamedTuple):
    text: str
    expected_text: str


class TestTextNormalizer:
    @pytest.fixture(scope="class")
    def text_normalizer(self) -> TextNormalizer:
        return TextNormalizer()

    @pytest.mark.parametrize(
        TextNormalizerTestCase._fields,
        [
            TextNormalizerTestCase(text="A", expected_text="A"),
            TextNormalizerTestCase(text="ｷﾞ", expected_text="ギ"),
        ],
        ids=["正規化する必要がない文字はそのまま出力されるケース", "半角カタカナが全角カタカナに変換されるケース"],
    )
    def test_call(self, text_normalizer: TextNormalizer, text: str, expected_text: str) -> None:
        assert text_normalizer(text) == expected_text
