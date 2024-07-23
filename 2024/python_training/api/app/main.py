from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.config import get_settings
from app.container import Container
from app.log import get_logger
from app.routers import cards, contacts, health

logger = get_logger(get_settings().log_level)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # dependency-injector が pydantic v2 に対応していないため、
    # BaseSettings から直接読み込む from_pydantic() は利用しない
    # https://github.com/ets-labs/python-dependency-injector/issues/726
    container.env_config.from_dict(get_settings().model_dump())
    container.init_resources()
    yield


def create_app() -> tuple[FastAPI, Container]:
    container = Container()
    app = FastAPI(
        title="person-similarity-api",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )
    app.include_router(health.router)
    app.include_router(cards.router)
    app.include_router(contacts.router)
    app.add_middleware(CorrelationIdMiddleware)
    return app, container


app, container = create_app()


@app.get("/api", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    return HTMLResponse(
        content="""
        <a href=\"api/redoc\">redoc</a><br>
        <a href=\"api/docs\">docs</a><br>
        <a href=\"api/openapi.json\">OpenAPI.json</a>
    """
    )
