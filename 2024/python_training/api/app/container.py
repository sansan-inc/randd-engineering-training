from dependency_injector import containers, providers

from app.config import get_settings
from app.repositories import (
    BatchResultLocalFileRepository,
    BatchResultRepository,
    BusinessCardLocalFileRepository,
    BusinessCardRepository,
)
from app.services import BatchResultService, BusinessCardService


class Container(containers.DeclarativeContainer):
    """
    DIコンテナ
    """

    wiring_config = containers.WiringConfiguration(modules=[".routers.cards", ".routers.contacts"])
    env_config = providers.Configuration()

    if get_settings().is_local:
        batch_result_repository = providers.Resource(BatchResultLocalFileRepository)
        business_card_repository = providers.Resource(BusinessCardLocalFileRepository)
    else:
        batch_result_repository = providers.Resource(
            BatchResultRepository,  # type: ignore[arg-type]
            batch_result_s3_url_base=get_settings().batch_result_s3_url_base,
        )
        business_card_repository = providers.Resource(BusinessCardRepository)  # type: ignore[arg-type]

    batch_result_service = providers.Factory(BatchResultService, repository=batch_result_repository)
    business_card_service = providers.Factory(BusinessCardService, repository=business_card_repository)
