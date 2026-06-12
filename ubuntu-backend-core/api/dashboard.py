import psutil
import time
from fastapi import APIRouter, Depends
from core.security import verify_token
from scripts.network_tunnel import get_tunnel_url, start_tunnel, stop_tunnel

# Nhập hàm trích xuất log từ database
from core.database import get_request_stats 

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(verify_token)] 
)

# Cơ sở dữ liệu tạm (RAM) lưu trạng thái API
api_status_db = {
    "internet_tunnel": {"active": False, "description": "Đường hầm Cloudflare bảo mật", "public_url": ""},
    "chatbox_ai": {"active": True, "description": "Module Chatbot AI & Phân tích Log", "public_url": ""},
    "social_db": {"active": True, "description": "Kết nối Database MariaDB Social Hub", "public_url": ""}
}

@router.get("/system-stats")
async def get_system_stats():
    """Lấy thông số phần cứng Real-time để vẽ biểu đồ lên Dashboard"""
    cpu_percent = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return {
        "status": "success",
        "cpu_usage_percent": cpu_percent,
        "ram": {
            "percent": ram.percent,
            "used_gb": round(ram.used / (1024**3), 2),
            "total_gb": round(ram.total / (1024**3), 2)
        },
        "storage": {
            "percent": disk.percent,
            "free_gb": round(disk.free / (1024**3), 2),
            "total_gb": round(disk.total / (1024**3), 2)
        }
    }

@router.get("/services")
async def get_services():
    """Lấy danh sách và trạng thái của các API Service"""
    # Nếu Tunnel đang bật, liên tục quét file log để lấy link public
    if api_status_db["internet_tunnel"]["active"] and not api_status_db["internet_tunnel"]["public_url"]:
        api_status_db["internet_tunnel"]["public_url"] = get_tunnel_url()
        
    return {"status": "success", "services": api_status_db}

@router.post("/services/toggle/{service_name}")
async def toggle_service(service_name: str):
    """Bật/Tắt công tắc của một dịch vụ API"""
    if service_name in api_status_db:
        current_state = api_status_db[service_name]["active"]
        new_state = not current_state
        api_status_db[service_name]["active"] = new_state
        
        if service_name == "internet_tunnel":
            if new_state:
                start_tunnel()
                # Ép hệ thống truy quét log liên tục để bắt link trả về UI ngay lập tức
                for _ in range(15):
                    time.sleep(0.2)
                    url = get_tunnel_url()
                    if url:
                        api_status_db["internet_tunnel"]["public_url"] = url
                        break
            else:
                stop_tunnel()
                api_status_db["internet_tunnel"]["public_url"] = ""
                
        return {
            "status": "success", 
            "message": f"Đã {'BẬT' if new_state else 'TẮT'} dịch vụ {service_name}", 
            "service": service_name, 
            "active": new_state
        }
    
    return {"status": "error", "message": "Dịch vụ không tồn tại trong hệ thống."}

@router.get("/analytics")
async def get_traffic_analytics():
    """Cung cấp dữ liệu Log thực tế để vẽ biểu đồ Traffic Chart"""
    try:
        # Lấy dữ liệu timeline từ database SQLite
        stats = get_request_stats()
        return {"status": "success", "data": stats["timeline"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}