from logging import getLogger

import gokart
import numpy as np
import pandas as pd
from pipeline.tasks.data_loader import LoadCardDataTask
from pipeline.utils.node2vec import SNAP
from pipeline.utils.template import GokartTask
from sklearn.preprocessing import LabelEncoder

logger = getLogger(__name__)


class CoOccurrenceMatrixCreationTask(GokartTask):
    """名刺交換履歴から共起行列を作る"""

    data_task: LoadCardDataTask = gokart.TaskInstanceParameter()

    def requires(self) -> LoadCardDataTask:
        return self.data_task

    def run(self) -> None:
        df = self.load_data_frame()
        co_occurrence_matrix, row_indexes = self.run_imp(df)
        self.dump((co_occurrence_matrix, row_indexes))

    @classmethod
    def run_imp(cls, df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
        # 隣接行列を作る前準備
        df["count"] = 1
        df_grouped = df.groupby(["user_id", "company_id"]).agg(count=("count", np.size))

        # 隣接行列を作ったとき、各行が対応するidentifierを記録
        row_indexes = df_grouped.reset_index()["user_id"].drop_duplicates().to_list()

        # 隣接行列
        adjacency_matrix = df_grouped.unstack().fillna(0).to_numpy()

        # 共起行列
        # SansanのAさん--他社X, SansanのBさん--他社Xというエッジがあるときに
        # A--Bのエッジを作成するため
        co_occurrence_matrix = np.dot(adjacency_matrix, adjacency_matrix.T)
        return co_occurrence_matrix, row_indexes


class EdgeListCreationTask(GokartTask):
    """共起行列からエッジリストを作る"""

    data_task: CoOccurrenceMatrixCreationTask = gokart.TaskInstanceParameter()

    def requires(self) -> CoOccurrenceMatrixCreationTask:
        return self.data_task

    def run(self) -> None:
        co_occurrence_matrix, row_indexes = self.load()
        df_edge = self.run_imp(co_occurrence_matrix, row_indexes)
        self.dump(df_edge)

    @classmethod
    def run_imp(cls, co_occurrence_matrix: np.ndarray, row_indexes: np.ndarray) -> pd.DataFrame:
        # 共起行列を用いてエッジリストの作成
        source_ids = []
        target_ids = []
        for i, vec in enumerate(co_occurrence_matrix):
            for j, value in enumerate(vec):
                if value > 0:
                    source_ids.append(row_indexes[i])
                    target_ids.append(row_indexes[j])

        df_edge = pd.DataFrame({"source_id": source_ids, "target_id": target_ids})

        # Self Loopの除去
        df_edge = df_edge.query("source_id != target_id").reset_index(drop=True)
        return df_edge


class FitEdgeLabelEncoderTask(GokartTask):
    """ノードに連番を振り、それを相互変換するEncoderの作成（pecanpyの仕様のため）"""

    data_task: EdgeListCreationTask = gokart.TaskInstanceParameter()

    def requires(self) -> EdgeListCreationTask:
        return self.data_task

    def run(self) -> None:
        df = self.load_data_frame()
        label_encoder = self.run_imp(df)
        self.dump(label_encoder)

    @classmethod
    def run_imp(cls, df: pd.DataFrame) -> LabelEncoder:
        edges = df["source_id"].tolist() + df["target_id"].tolist()
        edges = sorted(set(edges), key=edges.index)
        label_encoder = LabelEncoder()
        label_encoder.fit(edges)
        return label_encoder


class EdgeLabelEncodingTask(GokartTask):
    """user_idをEncoderで連番にする"""

    data_task: EdgeListCreationTask = gokart.TaskInstanceParameter()
    label_encoder_task: FitEdgeLabelEncoderTask = gokart.TaskInstanceParameter()

    def requires(self) -> dict[str, GokartTask]:
        return {
            "data": self.data_task,
            "label_encoder": self.label_encoder_task,
        }

    def run(self) -> None:
        df = self.load_data_frame("data")
        label_encoder = self.load("label_encoder")
        df = self.run_imp(df, label_encoder)
        self.dump(df)

    @classmethod
    def run_imp(cls, df: pd.DataFrame, label_encoder: LabelEncoder) -> pd.DataFrame:
        df["source_id"] = label_encoder.transform(df["source_id"].tolist())
        df["target_id"] = label_encoder.transform(df["target_id"].tolist())
        return df


class TrainNodeEmbeddingTask(GokartTask):
    """SNAPにより学習を行う"""

    data_task: EdgeLabelEncodingTask = gokart.TaskInstanceParameter()

    def requires(self) -> EdgeLabelEncodingTask:
        return self.data_task

    def run(self) -> None:
        df = self.load_data_frame()
        snap = self.run_imp(df)
        self.dump(snap)

    @classmethod
    def run_imp(cls, df: pd.DataFrame) -> SNAP:
        snap = SNAP()
        snap.fit(df)
        return snap


class PredictSimilarNodeTask(GokartTask):
    """類似人物の予測を行う"""

    data_task: EdgeListCreationTask = gokart.TaskInstanceParameter()
    model_task: TrainNodeEmbeddingTask = gokart.TaskInstanceParameter()
    label_encoder_task: FitEdgeLabelEncoderTask = gokart.TaskInstanceParameter()

    def requires(self) -> dict[str, GokartTask]:
        return {
            "data": self.data_task,
            "model": self.model_task,
            "encoder": self.label_encoder_task,
        }

    def run(self) -> None:
        # Load
        df = self.load_data_frame("data")
        model = self.load("model")
        label_encoder = self.load("encoder")

        response = self.run_imp(df, model, label_encoder)
        self.dump(response)

    @classmethod
    def run_imp(cls, df: pd.DataFrame, model: SNAP, label_encoder: LabelEncoder) -> dict[str, list]:
        df = df.drop_duplicates(subset="source_id")
        persons = list(set(df["source_id"].to_list()))

        # 類似人物を探す
        response = dict()
        for person in persons:
            node_id = label_encoder.transform([person])[0]
            similar_persons = label_encoder.inverse_transform(
                [int(index) for index, _ in model.w2v_model.wv.most_similar(node_id, topn=10)]
            )
            response[person] = similar_persons.tolist()

        return response
