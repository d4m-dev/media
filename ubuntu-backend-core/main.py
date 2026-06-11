import os
import sys
import uvicorn

# Ép hệ thống nhận diện thư mục gốc để không bị lỗi không tìm thấy module
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from api.server import app
from core.config import settings

if __name__ == "__main__":
    print(f"====================================================")
    print(f"🚀 KHỞI ĐỘNG HỆ THỐNG UBUNTU BACKEND CORE")
    print(f"🌐 Host: {settings.HOST}")
    print(f"🎯 Port: {settings.PORT}")
    print(f"⚙️ Môi trường: {settings.ENVIRONMENT.upper()}")
    print(f"📂 Thư mục gốc: {BASE_DIR}")
    print(f"====================================================")
    
    # Khởi chạy server FastAPI bằng Uvicorn trên cổng 16868
    uvicorn.run(
        "api.server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True if settings.ENVIRONMENT == "development" else False,
        log_level="info"
    )