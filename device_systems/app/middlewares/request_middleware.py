import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger("device_systems")


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        response: Response = await call_next(request)

        process_time = time.time() - start_time
        formatted_time = f"{process_time:.4f}"

        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Process-Time"] = formatted_time
        response.headers["X-Request-ID"] = request_id

        logger.info(
            f"METHOD={request.method} PATH={request.url.path} "
            f"STATUS={response.status_code} PROCESS_TIME={formatted_time}s "
            f"REQUEST_ID={request_id}"
        )

        return response
