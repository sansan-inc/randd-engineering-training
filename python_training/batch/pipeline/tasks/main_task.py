import luigi

from pipeline.tasks.data_handler import (
    CoOccurrenceMatrixCreationTask,
    EdgeLabelEncodingTask,
    EdgeListCreationTask,
    FitEdgeLabelEncoderTask,
    PredictSimilarNodeTask,
    TrainNodeEmbeddingTask,
)
from pipeline.tasks.data_loader import LoadCardDataTask
from pipeline.tasks.data_uploader import UploadPredictedDataTask
from pipeline.utils.template import GokartTask


class Main(GokartTask):
    output_athena_query_s3_url_base = luigi.Parameter()
    output_result_data_s3_url_base = luigi.Parameter()

    def requires(self) -> UploadPredictedDataTask:
        data_load_task = LoadCardDataTask(output_athena_query_s3_url_base=self.output_athena_query_s3_url_base)
        co_occurrence_matrix_creation_task = CoOccurrenceMatrixCreationTask(data_task=data_load_task)
        edge_list_creation_task = EdgeListCreationTask(data_task=co_occurrence_matrix_creation_task)
        fit_edge_label_encoder_task = FitEdgeLabelEncoderTask(data_task=edge_list_creation_task)
        edge_label_encoding_task = EdgeLabelEncodingTask(
            data_task=edge_list_creation_task,
            label_encoder_task=fit_edge_label_encoder_task,
        )
        train_node_embedding_task = TrainNodeEmbeddingTask(data_task=edge_label_encoding_task)
        predict_similar_node_task = PredictSimilarNodeTask(
            data_task=edge_list_creation_task,
            model_task=train_node_embedding_task,
            label_encoder_task=fit_edge_label_encoder_task,
        )
        upload_predict_data_task = UploadPredictedDataTask(
            predict_similar_node_task=predict_similar_node_task,
            output_result_data_s3_url_base=self.output_result_data_s3_url_base,
        )
        return upload_predict_data_task

    def run(self) -> None:
        self.dump("Finished !")
