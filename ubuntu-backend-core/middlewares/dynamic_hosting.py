import os
import sys
import importlib.util
from fastapi.responses import FileResponse, JSONResponse
from starlette.types import Scope, Receive, Send
from starlette.middleware.wsgi import WSGIMiddleware

# Bộ nhớ tạm (Cache) để lưu các ứng dụng Flask đã được tải vào RAM
_flask_app_cache = {}

# VÙNG AN TOÀN: Nơi chứa tất cả các dự án web con của bạn
HOSTING_DIR = "/storage/emulated/0/coder/media/ubuntu-backend-core/hosted_projects"

class DynamicHostingMiddleware:
    def __init__(self, app):
        self.app = app
        # Tự động tạo thư mục "vùng an toàn" nếu chưa có
        os.makedirs(HOSTING_DIR, exist_ok=True)

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        # Chỉ can thiệp vào các đường truyền HTTP
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        path = scope["path"]

        # 1. BỎ QUA - Trả lại quyền xử lý cho các API gốc của Backend (Dashboard, Websocket...)
        if path == "/" or path.startswith("/api/") or path.startswith("/ws/") or path.startswith("/css/") or path.startswith("/js/"):
            return await self.app(scope, receive, send)

        # 2. XỬ LÝ - Đón các request yêu cầu truy cập dự án con
        parts = [p for p in path.split("/") if p]
        if not parts:
            return await self.app(scope, receive, send)

        folder_name = parts[0]
        project_path = os.path.join(HOSTING_DIR, folder_name)

        # Kiểm tra xem có thư mục dự án tương ứng không
        if os.path.isdir(project_path):
            remaining_path = "/".join(parts[1:])
            file_target = os.path.join(project_path, remaining_path)

            # A) Trả file tĩnh (Hình ảnh, CSS, JS) nếu tồn tại trực tiếp
            if remaining_path and os.path.isfile(file_target) and not file_target.endswith('.py'):
                response = FileResponse(file_target)
                return await response(scope, receive, send)

            # B) Tìm và chạy file Python (Flask/WSGI)
            index_py_public = os.path.join(project_path, 'public', 'index.py')
            index_py = os.path.join(project_path, 'index.py')
            index_html = os.path.join(project_path, 'index.html')

            target_py = index_py_public if os.path.exists(index_py_public) else (index_py if os.path.exists(index_py) else None)

            if target_py:
                asgi_app = self.get_or_load_wsgi_app(target_py)
                if asgi_app:
                    # Quan trọng: Đổi gốc tọa độ SCRIPT_NAME để Flask định tuyến đúng URL
                    scope["root_path"] = f"/{folder_name}"
                    return await asgi_app(scope, receive, send)

            # C) Trả file HTML tĩnh nếu trong thư mục không có backend riêng
            if os.path.exists(index_html):
                response = FileResponse(index_html)
                return await response(scope, receive, send)

        # 3. LỖI - Gọi đường dẫn lạ không tồn tại dự án -> 404
        response = JSONResponse(status_code=404, content={"status": "error", "message": f"❌ Không tìm thấy dự án hoặc tệp tin tại /{folder_name}"})
        return await response(scope, receive, send)

    def get_or_load_wsgi_app(self, file_path):
        """Logic nạp Code động qua ImportLib (Chuyển thể nguyên bản từ file cũ)"""
        cache_key = os.path.abspath(file_path)
        if cache_key in _flask_app_cache:
            return _flask_app_cache[cache_key]

        try:
            module_name = f"hosted_app_{os.path.basename(os.path.dirname(file_path))}"
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None or spec.loader is None: return None

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module

            old_cwd = os.getcwd()
            old_sys_path = sys.path.copy()

            try:
                script_dir = os.path.dirname(os.path.abspath(file_path))
                os.chdir(script_dir)
                if script_dir not in sys.path:
                    sys.path.insert(0, script_dir)

                spec.loader.exec_module(module)

                # Lọc tìm đối tượng ứng dụng Flask
                flask_app = None
                if hasattr(module, 'app'): flask_app = module.app
                elif hasattr(module, 'application'): flask_app = module.application

                if flask_app:
                    # Tuyệt kỹ: Bọc WSGI (Đồng bộ) thành ASGI (Bất đồng bộ)
                    asgi_app = WSGIMiddleware(flask_app)
                    _flask_app_cache[cache_key] = asgi_app
                    return asgi_app
            finally:
                os.chdir(old_cwd)
                sys.path = old_sys_path
        except Exception as e:
            print(f"❌ Lỗi tải dự án động {file_path}: {e}")

        return None