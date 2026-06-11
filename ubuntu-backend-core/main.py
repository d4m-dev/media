import uvicorn
from core.config import settings
from scripts.network_tunnel import start_tunnel # Dùng module chuẩn thức

def start_system():
    print("="*50)
    print(f"🚀 KHỞI ĐỘNG HỆ THỐNG UBUNTU BACKEND CORE")
    print(f"📡 Local IP Access: http://192.168.110.2:{settings.PORT}")
    print(f"💻 Localhost: http://127.0.0.1:{settings.PORT}")
    print("="*50)
    
    # Tự động kích hoạt đường hầm mạng khi mở hệ thống
    print("🔄 Đang kiểm tra kết nối mạng bên ngoài...")
    start_tunnel()
    print("-" * 50)
    
    # Khởi động server API FastAPI
    uvicorn.run(
        "api.server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=(settings.ENVIRONMENT == "development")
    )

if __name__ == "__main__":
    try:
        start_system()
    except KeyboardInterrupt:
        print("\n🛑 Đã nhận lệnh tắt. Đang dọn dẹp hệ thống...")
        # (Tùy chọn: Bạn có thể gọi stop_tunnel() ở đây nếu muốn hệ thống tự ngắt mạng khi tắt server)
    except Exception as e:
        print(f"\n❌ Đã xảy ra lỗi nghiêm trọng: {e}")