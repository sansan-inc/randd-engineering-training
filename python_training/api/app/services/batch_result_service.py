from app.repositories import IBatchResultRepository


class BatchResultService:
    def __init__(self, repository: IBatchResultRepository) -> None:
        self._repository = repository

    def get_data(self) -> dict[str, list[str]]:
        return self._repository.get_data()
