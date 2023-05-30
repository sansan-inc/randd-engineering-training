from asgi_correlation_id import CorrelationIdMiddleware
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.config import get_setting
from app.container import Container
from app.log import get_logger
from app.routers import health, person

load_dotenv()
logger = get_logger(get_setting().log_level)


def create_app() -> tuple[FastAPI, Container]:
    container = Container()
    container.init_resources()
    app = FastAPI(title="app", version="0.1.0")
    app.include_router(health.router)
    app.include_router(person.router)
    app.add_middleware(CorrelationIdMiddleware)
    return app, container


app, container = create_app()


@app.on_event("startup")
async def startup_event() -> None:
    container.env_config.from_pydantic(get_setting())


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    return HTMLResponse(
        content="""
        <a href=\"redoc\">redoc</a><br>
        <a href=\"docs\">docs</a><br>
        <a href=\"openapi.json\">OpenAPI.json</a>
    """
    )
