import asyncio
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.database import log_request
from api.websockets import manager

class LoggerTrackerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Bóc tách thông tin thiết bị truy cập
        client_ip = request.client.host if request.client else "Unknown"
        method = request.method
        path = request.url.path
        
        # 2. Xử lý request để lấy mã trạng thái (200, 404, 500...)
        response = await call_next(request)
        status_code = response.status_code
        
        # 3. Lưu vào Database SQLite để AI SysAdmin đọc
        log_request(client_ip, method, path, status_code)
        
        # 4. Phát sóng thời gian thực (Real-time broadcast) cho Dashboard
        log_message = f"[{method}] {path} - Status: {status_code} - IP: {client_ip}"
        
        # Chạy tác vụ bắn log ngầm để không làm chậm luồng chính
        try:
            asyncio.create_task(manager.broadcast(log_message))
        except Exception:
            pass
        
        return response