import time
from starlette.middleware.base import BaseHTTPMiddleware
from ..utils import logger


# 记录请求日志
class LogerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        logger.info(f'{request.method} {request.url} completed_in={formatted_process_time}ms status_code={response.status_code}')
        return response
