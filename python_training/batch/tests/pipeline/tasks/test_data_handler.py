import numpy as np
import pandas as pd
import pytest
from pipeline.tasks.data_handler import CoOccurrenceMatrixCreationTask, FitEdgeLabelEncoderTask


class TestCoOccurrenceMatrixCreationTask:
    @pytest.mark.parametrize(
        ("data_frame", "expected_co_occurrence_matrix", "expected_row_indexes"),
        [
            (
                pd.DataFrame(
                    {
                        "user_id": ["a", "b", "c"],
                        "company_id": ["A", "B", "A"],
                    }
                ),
                [[1.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 1.0]],
                ["a", "b", "c"],
            )
        ],
    )
    def test_run_imp(
        self,
        data_frame: pd.DataFrame,
        expected_co_occurrence_matrix: list[list[float]],
        expected_row_indexes: list[str],
    ) -> None:
        co_occurrence_matrix, row_indexes = CoOccurrenceMatrixCreationTask.run_imp(df=data_frame)

        np.testing.assert_equal(co_occurrence_matrix, expected_co_occurrence_matrix)
        np.testing.assert_equal(row_indexes, expected_row_indexes)


class TestFitEdgeLabelEncoderTask:
    @pytest.mark.parametrize(
        ("data_frame", "input_labels", "expected_labels"),
        [
            (
                pd.DataFrame(
                    {
                        "source_id": ["a", "b", "c"],
                        "target_id": ["b", "d", "e"],
                    }
                ),
                ["a", "b", "c", "d", "e"],
                [0, 1, 2, 3, 4],
            ),
        ],
    )
    def test_run_imp(self, data_frame: pd.DataFrame, input_labels: list[str], expected_labels: list[int]) -> None:
        result = FitEdgeLabelEncoderTask.run_imp(df=data_frame)
        np.testing.assert_equal(result.transform(input_labels), expected_labels)
