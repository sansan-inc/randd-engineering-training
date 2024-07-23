from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["internal check endpoint"])


@router.get("/health", response_model=str, description="Health check endpoint")
def health() -> str:
    return "OK"
