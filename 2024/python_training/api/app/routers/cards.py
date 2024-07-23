from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.container import Container
from app.logging_and_timeout import LoggingAndTimeoutRoute
from app.schemas.cards import BusinessCardsResponse, SimilarBusinessCardsResponse
from app.services.batch_result_service import BatchResultService
from app.services.business_card_service import BusinessCardService

router = APIRouter(prefix="/api/cards", tags=["cards"], route_class=LoggingAndTimeoutRoute)
batch_result_service = Depends(Provide[Container.batch_result_service])
business_card_service = Depends(Provide[Container.business_card_service])


@router.get("/", response_model=BusinessCardsResponse, description="Get a list of business cards")
@inject
def list_business_cards(
    offset: int = Query(ge=0, default=0),
    limit: int = Query(ge=1, default=100),
    service: BusinessCardService = business_card_service,
) -> BusinessCardsResponse:
    result_df = service.get_business_card_df().iloc[offset : offset + limit]
    return BusinessCardsResponse.model_validate(result_df.to_dict(orient="records"))


@router.get("/count", response_model=int, description="Get the number of business cards")
@inject
def count_business_cards(service: BusinessCardService = business_card_service) -> int:
    return len(service.get_business_card_df())


@router.get("/{user_id}", response_model=BusinessCardsResponse, description="Get a business card of user_id")
@inject
def get_business_card(user_id: str, service: BusinessCardService = business_card_service) -> BusinessCardsResponse:
    result_df = service.get_business_card_df().query(f"user_id == '{user_id}'")
    return BusinessCardsResponse.model_validate(result_df.to_dict(orient="records"))


@router.get(
    "/{user_id}/similar_top10_users",
    response_model=SimilarBusinessCardsResponse | None,
    description="Get the top 10 similar users of the user with user_id",
)
@inject
def search_similar_person(
    user_id: str,
    batch_result_service: BatchResultService = batch_result_service,
    business_card_service: BusinessCardService = business_card_service,
) -> SimilarBusinessCardsResponse:
    results = batch_result_service.get_similar_persons()
    similar_persons = results.get(user_id)
    if similar_persons is None:
        return SimilarBusinessCardsResponse.model_validate([])
    user_ids, scores = zip(*[[person["user_id"], person["similarity"]] for person in similar_persons], strict=True)
    result_df = business_card_service.get_business_card_df()
    result_df = result_df[result_df["user_id"].isin(user_ids)]
    result_df = result_df.assign(similarity=scores)
    return SimilarBusinessCardsResponse.model_validate(result_df.to_dict(orient="records"))
