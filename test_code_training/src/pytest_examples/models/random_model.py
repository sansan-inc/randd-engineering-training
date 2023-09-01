import random
import time

from pytest_examples.schemas.model_output import ModelOutput


class RandomModel:
    """機械学習モデルを想定したクラス"""

    def __init__(self) -> None:
        time.sleep(5)  # 非常に重い初期化処理を想定している

        self.start_weight = random.uniform(0, 1)
        self.end_weight = random.uniform(self.start_weight, 1)

    def predict(self, text: str) -> ModelOutput:
        """
        テキストから抽出したい部分の開始と終了位置を予測するメソッド

        Args:
            text: 抽出対象のテキスト

        Returns:
            予測結果
        """
        start_position = self._decision_start_position(text)
        end_position = self._decision_end_position(text)
        return ModelOutput(text_length=len(text), start_position=start_position, end_position=end_position)

    def _decision_start_position(self, text: str) -> int:
        """
        Args:
            text: 抽出対象のテキスト

        Returns:
            抽出したい部分の開始位置
        """
        return int(len(text) * self.start_weight)

    def _decision_end_position(self, text: str) -> int:
        """
        Args:
            text: 抽出対象のテキスト

        Returns:
            抽出したい部分の終了位置
        """
        return int(len(text) * self.end_weight)
