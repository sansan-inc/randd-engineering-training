from app.repositories import IBatchResultRepository


class BatchResultService:
    def __init__(self, repository: IBatchResultRepository) -> None:
        self._repository = repository

    def get_similar_persons(self) -> dict[str, list[dict]]:
        return self._repository.similar_persons
