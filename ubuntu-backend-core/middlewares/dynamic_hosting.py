import os
import sys
import importlib.util
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, HTMLResponse
from starlette.types import Scope, Receive, Send

try:
    from starlette.middleware.wsgi import WSGIMiddleware
except ImportError:
    WSGIMiddleware = None

_flask_app_cache = {}
HOSTING_DIR = "/storage/emulated/0/coder/media/ubuntu-backend-core/hosted_projects"

class DynamicHostingMiddleware:
    def __init__(self, app):
        self.app = app
        os.makedirs(HOSTING_DIR, exist_ok=True)

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        path = scope["path"]

        # Cho phép các tài nguyên hệ thống đi qua
        if (path == "/" or path.startswith("/api/") or path.startswith("/ws/") or 
            path.startswith("/css/") or path.startswith("/js/") or path.startswith("/audio-files/") or 
            path.startswith("/admin/") or path.endswith(".html")):
            return await self.app(scope, receive, send)

        parts = [p for p in path.split("/") if p]
        if not parts:
            return await self.app(scope, receive, send)

        folder_name = parts[0]
        project_path = os.path.join(HOSTING_DIR, folder_name)

        if os.path.isdir(project_path):
            if os.path.exists(os.path.join(project_path, ".frozen")):
                response = JSONResponse(status_code=503, content={"status": "error", "message": f"❄️ Dự án '{folder_name}' đang đóng băng!"})
                await response(scope, receive, send) # 🚀 FIX: Chuẩn ASGI
                return

            if len(parts) == 1 and not path.endswith("/"):
                redirect_url = f"{path}/"
                if scope.get("query_string"): 
                    redirect_url += f"?{scope['query_string'].decode()}"
                response = RedirectResponse(url=redirect_url, status_code=307)
                await response(scope, receive, send) # 🚀 FIX: Chuẩn ASGI
                return

            remaining_path = "/".join(parts[1:])
            file_target = os.path.join(project_path, remaining_path)

            if remaining_path and os.path.isfile(file_target) and not file_target.endswith('.py'):
                response = FileResponse(file_target)
                await response(scope, receive, send) # 🚀 FIX: Chuẩn ASGI
                return

            # Ưu tiên load HTML nếu có
            index_html = os.path.join(project_path, 'index.html')
            if not remaining_path or remaining_path == 'index.html':
                if os.path.exists(index_html):
                    response = FileResponse(index_html)
                    await response(scope, receive, send) # 🚀 FIX: Chuẩn ASGI
                    return
                    
            # Load Python WSGI
            index_py_public = os.path.join(project_path, 'public', 'index.py')
            index_py = os.path.join(project_path, 'index.py')
            target_py = index_py_public if os.path.exists(index_py_public) else (index_py if os.path.exists(index_py) else None)

            if target_py and WSGIMiddleware:
                try:
                    asgi_app = self.get_or_load_wsgi_app(target_py)
                    if asgi_app:
                        scope["root_path"] = f"/{folder_name}"
                        return await asgi_app(scope, receive, send)
                except Exception as e:
                    print(f"Lỗi khởi chạy Python Project: {e}")

        # Lỗi 404
        response = JSONResponse(status_code=404, content={"status": "error", "message": f"❌ Không tìm thấy tài nguyên: {path}"})
        await response(scope, receive, send) # 🚀 FIX: Chuẩn ASGI
        return

    def get_or_load_wsgi_app(self, file_path):
        if not WSGIMiddleware: return None
        cache_key = os.path.abspath(file_path)
        if cache_key in _flask_app_cache: return _flask_app_cache[cache_key]
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
                if script_dir not in sys.path: sys.path.insert(0, script_dir)
                spec.loader.exec_module(module)
                flask_app = getattr(module, 'app', getattr(module, 'application', None))
                if flask_app:
                    asgi_app = WSGIMiddleware(flask_app)
                    _flask_app_cache[cache_key] = asgi_app
                    return asgi_app
            finally:
                os.chdir(old_cwd)
                sys.path = old_sys_path
        except Exception as e: print(f"❌ Lỗi tải WSGI: {e}")
        return None