import asyncio
import datetime
import json
import time
import traceback
from collections.abc import Callable
from typing import Any

from fastapi import Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from starlette.exceptions import HTTPException as StarletteHTTPException
from structlog import get_logger

from app.config import get_settings

logger = get_logger()


class LoggingAndTimeoutRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response | None:
            response = None
            request_record = await self._get_request_logging_record(request)
            logger.info("request", ctx=request_record)

            response_record: dict = {}
            # 処理にかかる時間を計測
            before = time.time()
            try:
                response = await self._execute_request(request, original_route_handler, response_record)
            finally:
                duration = round(time.time() - before, 4)
                time_local = datetime.datetime.fromtimestamp(before)
                response_record["time_local"] = time_local.strftime("%Y/%m/%d %H:%M:%S%Z")
                response_record["processing_time_seconds"] = str(duration)
                response_record.update(await self._get_response_logging_record(response))
                logger.info("response", ctx=response_record)

            return response

        return custom_route_handler

    async def _execute_request(self, request: Request, route_handler: Callable, record: dict) -> Response:
        try:
            response: Response = await self._wait_for_request(request, route_handler)
        except StarletteHTTPException as exc:
            record["error"] = exc.detail
            record["status"] = exc.status_code
            record["traceback"] = traceback.format_exc().splitlines()
            if exc.status_code == status.HTTP_504_GATEWAY_TIMEOUT:
                # 意図して出しているため、トレースバックは含めない
                record["traceback"] = []
            raise
        except RequestValidationError as exc:
            # エラー内容を見ればわかるため、トレースバックは含めない
            record["error"] = exc.errors()
            record["status"] = status.HTTP_422_UNPROCESSABLE_ENTITY
            record["traceback"] = []
            raise
        return response

    async def _wait_for_request(self, request: Request, route_handler: Callable) -> Response:
        try:
            return await asyncio.wait_for(route_handler(request), timeout=get_settings().request_timeout)
        except asyncio.TimeoutError:
            raise StarletteHTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Request processing time exceeded limit"
            ) from None

    async def _get_request_logging_record(self, request: Request) -> dict[str, Any]:
        record: dict = {}
        if await request.body():
            try:
                record["request_body"] = await request.json()
            except json.JSONDecodeError:
                record["request_body"] = (await request.body()).decode("utf-8")

        record["remote_addr"] = None if request.client is None else request.client.host
        q_params = str(request.query_params)
        record["request_uri"] = request.url.path + "?" + q_params if q_params else request.url.path
        record["request_method"] = request.method
        return record

    async def _get_response_logging_record(self, response: Response | None) -> dict[str, Any]:
        record: dict = {}
        if response is None:
            return record
        try:
            record["response_body"] = json.loads(response.body.decode("utf-8"))
        except json.JSONDecodeError:
            record["response_body"] = response.body.decode("utf-8")
        record["status"] = response.status_code
        record["response_headers"] = {k.decode("utf-8"): v.decode("utf-8") for (k, v) in response.headers.raw}
        return record
