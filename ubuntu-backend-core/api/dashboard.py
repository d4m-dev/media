from fastapi import APIRouter, Depends, HTTPException
import psutil
import platform
import os
from core.security import verify_token
from scripts.network_tunnel import start_tunnel, stop_tunnel, get_public_url
from core.database import get_request_stats # Import hàm lấy dữ liệu biểu đồ

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(verify_token)] 
)

tunnel_is_active = os.path.exists("/storage/emulated/0/coder/media/ubuntu-backend-core/core/.tunnel.pid")
current_tunnel_url = get_public_url() if tunnel_is_active else None

api_status_db = {
    "internet_tunnel": {"active": tunnel_is_active, "description": "Kết nối Cloudflare đưa cổng 16868 ra Internet", "public_url": current_tunnel_url},
    "chatbox_ai": {"active": True, "description": "API xử lý ngôn ngữ và quản lý tài nguyên AI", "public_url": None},
    "social_db": {"active": True, "description": "API truy vấn cơ sở dữ liệu MariaDB", "public_url": None}
}

@router.get("/system-stats")
async def get_system_stats():
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/storage/emulated/0/' if os.path.exists('/storage/emulated/0/') else '/')
    return {
        "os": platform.system(),
        "cpu_usage_percent": psutil.cpu_percent(interval=0.1),
        "ram": {
            "total_gb": round(ram.total / (1024 ** 3), 2),
            "used_gb": round(ram.used / (1024 ** 3), 2),
            "percent": ram.percent
        },
        "storage": {
            "total_gb": round(disk.total / (1024 ** 3), 2),
            "free_gb": round(disk.free / (1024 ** 3), 2),
            "percent": disk.percent
        }
    }

@router.get("/services")
async def get_services_status():
    if api_status_db["internet_tunnel"]["active"]:
        api_status_db["internet_tunnel"]["public_url"] = get_public_url()
    else:
        api_status_db["internet_tunnel"]["public_url"] = None
    return {"services": api_status_db}

@router.post("/services/toggle/{service_name}")
async def toggle_service(service_name: str):
    if service_name not in api_status_db:
        raise HTTPException(status_code=404, detail="Không tìm thấy dịch vụ này")
        
    current_status = api_status_db[service_name]["active"]
    new_status = not current_status
    public_url = None
    
    if service_name == "internet_tunnel":
        if new_status: success, public_url = start_tunnel()
        else: success = stop_tunnel()
        if not success: raise HTTPException(status_code=500, detail="Lỗi Tunnel")
            
    api_status_db[service_name]["active"] = new_status
    api_status_db[service_name]["public_url"] = public_url
    return {"status": "success", "service": service_name, "is_active": new_status, "public_url": public_url}

# --- API BIỂU ĐỒ (MỚI) ---
@router.get("/analytics")
async def get_analytics_data():
    """API cung cấp dữ liệu cho biểu đồ Chart.js"""
    return get_request_stats()