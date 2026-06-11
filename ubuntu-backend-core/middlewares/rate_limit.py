from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import time

RATE_LIMIT_DURATION = 60
RATE_LIMIT_REQUESTS = 60

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.ip_records = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        path = request.url.path

        # Bỏ qua giới hạn chống Spam cho các dịch vụ thời gian thực
        if path.startswith("/api/dashboard/system-stats") or \
           path.startswith("/api/dashboard/analytics") or \
           path.startswith("/ws/"):
            return await call_next(request)

        # Dọn dẹp bộ đếm thời gian
        if client_ip in self.ip_records:
            self.ip_records[client_ip] = [
                timestamp for timestamp in self.ip_records[client_ip]
                if current_time - timestamp < RATE_LIMIT_DURATION
            ]
        else:
            self.ip_records[client_ip] = []

        # Chặn nếu gọi quá số lần quy định
        if len(self.ip_records[client_ip]) >= RATE_LIMIT_REQUESTS:
            return JSONResponse(
                status_code=429,
                content={"status": "error", "message": "⚠️ Quá nhiều yêu cầu. Vui lòng thử lại sau 1 phút!"}
            )

        self.ip_records[client_ip].append(current_time)
        return await call_next(request)