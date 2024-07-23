import datetime

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.container import Container
from app.logging_and_timeout import LoggingAndTimeoutRoute
from app.schemas.contacts import ContactHistoriesResponse
from app.services.business_card_service import BusinessCardService

router = APIRouter(prefix="/api/contacts", tags=["contacts"], route_class=LoggingAndTimeoutRoute)
business_card_service = Depends(Provide[Container.business_card_service])


@router.get("/", response_model=ContactHistoriesResponse, description="Get a list of contact histories")
@inject
def list_contact_history(
    offset: int = Query(ge=0, default=0),
    limit: int = Query(ge=1, default=100),
    start_date: datetime.date | None = None,
    end_date: datetime.date | None = None,
    service: BusinessCardService = business_card_service,
) -> ContactHistoriesResponse:
    result_df = service.get_contacts_df(start_date=start_date, end_date=end_date)
    result_df = result_df.iloc[offset : offset + limit]

    return ContactHistoriesResponse.model_validate(result_df.to_dict(orient="records"))


@router.get("/count", response_model=int, description="Get the number of contact histories")
@inject
def count_contact_history(
    start_date: datetime.date | None = None,
    end_date: datetime.date | None = None,
    service: BusinessCardService = business_card_service,
) -> int:
    result_df = service.get_contacts_df(start_date=start_date, end_date=end_date)
    return len(result_df)


@router.get(
    "/owner_users/{owner_user_id}",
    response_model=ContactHistoriesResponse,
    description="Get a list of contact histories by owner_user_id",
)
@inject
def list_contact_history_by_owner_user(  # noqa: PLR0913
    owner_user_id: str,
    offset: int = Query(ge=0, default=0),
    limit: int = Query(ge=1, default=100),
    start_date: datetime.date | None = None,
    end_date: datetime.date | None = None,
    service: BusinessCardService = business_card_service,
) -> ContactHistoriesResponse:
    result_df = service.get_contacts_df(start_date=start_date, end_date=end_date)
    result_df = result_df.query(f"owner_user_id == '{owner_user_id}'").iloc[offset : offset + limit]

    return ContactHistoriesResponse.model_validate(result_df.to_dict(orient="records"))


@router.get(
    "/owner_users/{owner_user_id}/count",
    response_model=int,
    description="Get the number of contact histories by owner_user_id",
)
@inject
def count_contact_history_by_owner_users(
    owner_user_id: str,
    start_date: datetime.date | None = None,
    end_date: datetime.date | None = None,
    service: BusinessCardService = business_card_service,
) -> int:
    result_df = service.get_contacts_df(start_date=start_date, end_date=end_date)
    result_df = result_df.query(f"owner_user_id == '{owner_user_id}'")

    return len(result_df)


@router.get(
    "/owner_companies/{owner_company_id}",
    response_model=ContactHistoriesResponse,
    description="Get a list of contact histories by owner_company_id",
)
@inject
def list_contact_history_by_owner_company(  # noqa: PLR0913
    owner_company_id: str,
    offset: int = Query(ge=0, default=0),
    limit: int = Query(ge=1, default=100),
    start_date: datetime.date | None = None,
    end_date: datetime.date | None = None,
    service: BusinessCardService = business_card_service,
) -> ContactHistoriesResponse:
    result_df = service.get_contacts_df(start_date=start_date, end_date=end_date)
    result_df = result_df.query(f"owner_company_id == '{owner_company_id}'").iloc[offset : offset + limit]

    return ContactHistoriesResponse.model_validate(result_df.to_dict(orient="records"))


@router.get(
    "/owner_companies/{owner_company_id}/count",
    response_model=int,
    description="Get the number of contact histories by owner_company_id",
)
@inject
def count_contact_history_by_owner_company(
    owner_company_id: str,
    start_date: datetime.date | None = None,
    end_date: datetime.date | None = None,
    service: BusinessCardService = business_card_service,
) -> int:
    result_df = service.get_contacts_df(start_date=start_date, end_date=end_date)
    result_df = result_df.query(f"owner_company_id == '{owner_company_id}'")

    return len(result_df)
