from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.database import log_request
from api.websockets import manager
import time
from datetime import datetime

class LoggerTrackerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        path = request.url.path
        method = request.method
        
        # Bỏ qua việc in log cho các API chạy liên tục ngầm (tránh rác màn hình)
        if path.startswith("/api/dashboard/system-stats") or path.startswith("/api/dashboard/analytics"):
            return await call_next(request)

        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = round((time.time() - start_time) * 1000, 2)
        status_code = response.status_code
        
        # Lưu vào cơ sở dữ liệu (SQLite)
        log_request(client_ip, method, path, status_code)
        
        # Bắn log realtime qua WebSocket cho Terminal trên Web
        current_time = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{current_time}] {client_ip} | {method} {path} | {status_code} | {process_time}ms"
        
        import asyncio
        asyncio.create_task(manager.broadcast(log_message))
        
        return response