from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.container import Container
from app.logging_context import LoggingContextRoute
from app.schemas.person import Persons
from app.services.batch_result_service import BatchResultService

router = APIRouter(prefix="/persons", tags=["persons"], route_class=LoggingContextRoute)


@router.get("/{person_name}", response_model=Persons)
@inject
def search_similar_person(
    person_name: str, service: BatchResultService = Depends(Provide[Container.batch_result_service])
) -> Persons:
    results = service.get_data()
    similar_persons = results.get(person_name)
    if similar_persons is None:
        return Persons(names=[])
    return Persons(names=similar_persons)


@router.get("/", response_model=Persons)
@inject
def list_persons(
    limit: int = 100, service: BatchResultService = Depends(Provide[Container.batch_result_service])
) -> Persons:
    results = service.get_data()
    persons = list(results.keys())[:limit]
    return Persons(names=persons)
