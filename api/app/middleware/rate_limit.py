import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 20, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.ip_store = {}
    
    async def dispatch(self, request: Request, call_next) -> Response:
        client_ip = request.client.host
        now_time = time.time()

        timestamps = self.ip_store.get(client_ip, [])
        timestamps = [t for t in timestamps if now_time - t < self.window_seconds]

        if len(timestamps) >= self.max_requests:
            return PlainTextResponse("Too many requests.", status_code=429)

        timestamps.append(now_time)
        self.ip_store[client_ip] = timestamps

        return await call_next(request)