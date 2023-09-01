import pytest

from pytest_examples.models.random_model import RandomModel
from pytest_examples.schemas.model_output import ModelOutput


class TestRandomModel:
    @pytest.fixture(scope="class")  # 時間のかかるインスタンス化もTestRandomModel内で1回行えば良いことになる
    def random_model(self) -> RandomModel:
        model = RandomModel()
        model.start_weight = 0.1
        model.end_weight = 0.7
        return model

    @pytest.mark.parametrize(
        ("text", "expected_start_position"),
        [
            ("Sansan株式会社", 1),
            ("33株式会社" * 10, 6),
            ("33株式会社" * 10 + "。", 6),
        ],
    )
    def test_decision_start_position(
        self,
        random_model: RandomModel,
        text: str,
        expected_start_position: int,
    ) -> None:
        assert random_model._decision_start_position(text) == expected_start_position

    @pytest.mark.parametrize(
        ("text", "expected_end_position"),
        [
            ("Sansan株式会社", 7),
            ("33株式会社" * 10, 42),
            ("33株式会社" * 10 + "。", 42),
        ],
    )
    def test_decision_end_position(
        self,
        random_model: RandomModel,
        text: str,
        expected_end_position: int,
    ) -> None:
        assert random_model._decision_end_position(text) == expected_end_position

    @pytest.mark.parametrize(
        ("text", "expected_model_output"),
        [
            (".Sansan株式会社", ModelOutput(text_length=11, start_position=1, end_position=7)),
            (".Yonyon株式会社", ModelOutput(text_length=11, start_position=1, end_position=7)),
        ],
    )
    def test_predict(self, random_model: RandomModel, text: str, expected_model_output: ModelOutput) -> None:
        assert random_model.predict(text) == expected_model_output
