
import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from starlette.requests import Request
from starlette.responses import Response

import logging

logging.basicConfig(level= logging.INFO,
                     format='%(asctime)s [%(levelname)s] trace_id=%(trace_id)s %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ])
logger = logging.getLogger(__name__)


class TraceabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id
        logger = logging.LoggerAdapter(logging.getLogger(__name__), {"trace_id": trace_id})
        logger.info(f"Request method={request.method} path={request.url.path}")
        response = await call_next(request)
        response.headers["X-Trace-ID"] = trace_id
        logger.info(f"Response status_code={response.status_code}")
        return response
    

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        trace_id = request.state.trace_id if hasattr(request.state, 'trace_id') else None
        logger.info(f"Request trace_id={trace_id} method={request.method} path={request.url.path}")
        response = await call_next(request)
        logger.info(f"Response trace_id={trace_id} status_code={response.status_code}")
        return response