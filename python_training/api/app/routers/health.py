from fastapi import APIRouter

router = APIRouter(tags=["internal check endpoint"])


@router.get("/health", response_model=str)
def health() -> str:
    return "OK"
