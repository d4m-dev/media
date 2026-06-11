import asyncio
from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import subprocess
import os

router = APIRouter(
    prefix="/api/ws",
    tags=["WebSockets"]
)

# ==========================================
# 1. QUẢN LÝ KẾT NỐI WEBSOCKET CHO LOGS (Dashboard)
# ==========================================
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """Bắn thông điệp (log) tới tất cả các client đang kết nối"""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

# 🚀 Khởi tạo biến manager để logger_tracker.py có thể import
manager = ConnectionManager()

@router.websocket("/logs")
async def websocket_logs(websocket: WebSocket):
    """Endpoint nhận kết nối để xem log realtime trên giao diện"""
    await manager.connect(websocket)
    try:
        while True:
            # Giữ kết nối sống để liên tục nhận dữ liệu
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# ==========================================
# 2. XỬ LÝ KẾT NỐI TERMINAL (Giao diện dòng lệnh)
# ==========================================
@router.websocket("/terminal")
async def terminal_websocket(websocket: WebSocket):
    """Endpoint xử lý lệnh từ Terminal trên Dashboard"""
    await websocket.accept()
    await websocket.send_text("✅ [Hệ thống] Đã kết nối Terminal bảo mật tại Port 16868.\n")
    try:
        while True:
            # Nhận lệnh từ Frontend
            data = await websocket.receive_text()
            if not data.strip():
                continue
                
            # Thực thi lệnh trực tiếp trên Ubuntu
            try:
                process = await asyncio.create_subprocess_shell(
                    data,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd="/storage/emulated/0/coder/media/ubuntu-backend-core"
                )
                stdout, stderr = await process.communicate()
                
                if stdout:
                    await websocket.send_text(stdout.decode('utf-8'))
                if stderr:
                    await websocket.send_text(f"LỖI: {stderr.decode('utf-8')}")
                
                # In ra dấu nhắc lệnh mới
                await websocket.send_text("\nroot@d4m-backend:~# ")
                
            except Exception as e:
                await websocket.send_text(f"Lỗi thực thi: {str(e)}\nroot@d4m-backend:~# ")
                
    except WebSocketDisconnect:
        print("Terminal WebSocket disconnected")