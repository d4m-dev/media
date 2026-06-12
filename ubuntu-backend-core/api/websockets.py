import asyncio
import os
from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/api/ws", tags=["WebSockets"])

# Tự động nhận diện thư mục gốc để tránh lỗi Crash khi Terminal chạy lệnh
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

@router.websocket("/logs")
async def websocket_logs(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.websocket("/terminal")
async def terminal_websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("✅ [Hệ thống] Đã kết nối Terminal bảo mật tại Port 16868.\nroot@d4m-backend:~# ")
    try:
        while True:
            data = await websocket.receive_text()
            if not data.strip(): continue
            try:
                # Sử dụng đường dẫn động thay vì gán cứng
                process = await asyncio.create_subprocess_shell(
                    data,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=BASE_DIR 
                )
                stdout, stderr = await process.communicate()
                
                if stdout: await websocket.send_text(stdout.decode('utf-8'))
                if stderr: await websocket.send_text(f"LỖI: {stderr.decode('utf-8')}")
                
                await websocket.send_text("\nroot@d4m-backend:~# ")
            except Exception as e:
                await websocket.send_text(f"Lỗi thực thi: {str(e)}\nroot@d4m-backend:~# ")
    except WebSocketDisconnect:
        pass