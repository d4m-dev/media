import os
import json
import math
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/projects",
    tags=["Project Hub"]
)

HOSTING_DIR = "/storage/emulated/0/coder/media/ubuntu-backend-core/hosted_projects"

def get_dir_size(path):
    """Tính tổng dung lượng đệ quy của thư mục"""
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total += os.path.getsize(fp)
    return total

def format_size(size_bytes):
    """Định dạng dung lượng sang KB, MB"""
    if size_bytes == 0: return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

@router.get("/")
async def scan_projects():
    """Quét và trả về danh sách các dự án đang được Host"""
    os.makedirs(HOSTING_DIR, exist_ok=True)
    projects = []
    
    for folder in os.listdir(HOSTING_DIR):
        folder_path = os.path.join(HOSTING_DIR, folder)
        if os.path.isdir(folder_path):
            # 1. Tính dung lượng
            size_bytes = get_dir_size(folder_path)
            size_str = format_size(size_bytes)
            
            # 2. Phân loại công nghệ
            has_python = os.path.exists(os.path.join(folder_path, "index.py")) or os.path.exists(os.path.join(folder_path, "public", "index.py"))
            has_html = os.path.exists(os.path.join(folder_path, "index.html"))
            
            # 3. Tìm ảnh bìa (Smart Thumbnail)
            thumbnail = None
            for ext in ["png", "jpg", "jpeg", "webp"]:
                if os.path.exists(os.path.join(folder_path, f"preview.{ext}")):
                    thumbnail = f"/{folder}/preview.{ext}"
                    break
                elif os.path.exists(os.path.join(folder_path, f"cover.{ext}")):
                    thumbnail = f"/{folder}/cover.{ext}"
                    break
            
            # 4. Trích xuất mô tả tự động
            description = "Dự án mới triển khai. Chưa có mô tả."
            info_path = os.path.join(folder_path, "info.txt")
            pkg_path = os.path.join(folder_path, "package.json")
            
            if os.path.exists(info_path):
                with open(info_path, "r", encoding="utf-8") as f:
                    description = f.read().strip()
            elif os.path.exists(pkg_path):
                try:
                    with open(pkg_path, "r", encoding="utf-8") as f:
                        pkg = json.load(f)
                        if "description" in pkg: description = pkg["description"]
                except: pass
            
            projects.append({
                "name": folder,
                "size": size_str,
                "has_python": has_python,
                "has_html": has_html,
                "thumbnail": thumbnail,
                "description": description
            })
            
    return {"status": "success", "count": len(projects), "projects": projects}