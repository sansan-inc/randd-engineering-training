from dependency_injector import containers, providers

from app.repositories import BatchResultLocalFileRepository, BatchResultRepository
from app.services import BatchResultService


class Container(containers.DeclarativeContainer):
    """
    DIコンテナ
    """

    wiring_config = containers.WiringConfiguration(modules=[".routers.person"])

    env_config = providers.Configuration()

    batch_result_repository = providers.Selector(
        env_config.is_local,
        true=providers.Singleton(BatchResultLocalFileRepository),
        false=providers.Singleton(BatchResultRepository, batch_result_s3_url_base=env_config.batch_result_s3_url_base),
    )

    batch_result_service = providers.Singleton(BatchResultService, repository=batch_result_repository)
