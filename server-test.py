#!/usr/bin/env python3
"""
Server đa năng - Chạy cả Flask apps (.py), file .html và quản lý phpMyAdmin
Port chính: 1515
Hỗ trợ: /storage/emulated/0/...
"""

import os
import sys
import subprocess
import threading
import re
import atexit
import mimetypes
import requests
import importlib.util
from wsgiref.simple_server import make_server, WSGIRequestHandler
import socket
import json
from collections import deque

class TerminalLogBuffer:
    def __init__(self, maxlen=5000):
        self.buffer = deque(maxlen=maxlen)
        self.lock = threading.Lock()
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

    def write(self, text):
        self.original_stdout.write(text)
        with self.lock:
            self.buffer.append(text)

    def write_err(self, text):
        self.original_stderr.write(text)
        with self.lock:
            self.buffer.append(text)

    def flush(self):
        self.original_stdout.flush()

    def flush_err(self):
        self.original_stderr.flush()

    def get_logs(self, start=0):
        with self.lock:
            # Nếu start vượt quá số lượng, hoặc client yêu cầu số âm (ví dụ lỗi), tải lại từ đầu hoặc phần cuối
            logs_list = list(self.buffer)
            if start > len(logs_list):
                return [], len(logs_list)
            return logs_list[start:], len(logs_list)

terminal_logs = TerminalLogBuffer()

class StdoutProxy:
    def write(self, text):
        terminal_logs.write(text)
    def flush(self):
        terminal_logs.flush()
    def __getattr__(self, name):
        return getattr(terminal_logs.original_stdout, name)

class StderrProxy:
    def write(self, text):
        terminal_logs.write_err(text)
    def flush(self):
        terminal_logs.flush_err()
    def __getattr__(self, name):
        return getattr(terminal_logs.original_stderr, name)

sys.stdout = StdoutProxy()
sys.stderr = StderrProxy()

# Đảm bảo script luôn chạy từ thư mục chứa nó
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# Thêm BASE_DIR vào sys.path
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# --- CẤU HÌNH ---
PORT = 25151
PHPMYADMIN_PORT = 1212 # Chạy phpMyAdmin trên port riêng để tránh xung đột WSGI
PHPMYADMIN_DIR_NAME = os.path.expanduser("~/phpmyadmin") # Tên thư mục chứa phpmyadmin của bạn
CLOUDFLARE_BIN = os.path.join(os.environ.get('HOME', '.'), "cloudflared-linux-arm64")

# Cache & Process Management
_flask_app_cache = {}
tunnel_process = None
php_process = None


class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'


def load_flask_app_from_py(file_path):
    if not os.path.isabs(file_path):
        file_path = os.path.normpath(os.path.join(BASE_DIR, file_path))
    
    cache_key = os.path.abspath(file_path)
    if cache_key in _flask_app_cache:
        return _flask_app_cache[cache_key]
    
    if not os.path.exists(file_path):
        return None
    
    try:
        module_name = f"app_{os.path.basename(file_path).replace('.py', '').replace('-', '_')}"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            return None
        
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
            
            flask_app = None
            if hasattr(module, 'app'):
                flask_app = module.app
            elif hasattr(module, 'application'):
                flask_app = module.application
            
            if flask_app is not None:
                result = (flask_app, script_dir)
                _flask_app_cache[cache_key] = result
                return result
        finally:
            os.chdir(old_cwd)
            sys.path = old_sys_path
    except Exception as e:
        print(f"{Colors.RED}❌ Lỗi load Flask app: {e}{Colors.RESET}")
    return None


def create_flask_proxy(flask_app, script_dir, base_path):
    def proxy_app(environ, start_response):
        old_cwd = os.getcwd()
        old_sys_path = sys.path.copy()
        
        try:
            os.chdir(script_dir)
            if script_dir not in sys.path:
                sys.path.insert(0, script_dir)
            
            new_environ = environ.copy()
            new_environ['SCRIPT_NAME'] = base_path
            new_environ['SERVER_NAME'] = 'localhost'
            new_environ['SERVER_PORT'] = str(PORT)
            
            return flask_app(new_environ, start_response)
        finally:
            os.chdir(old_cwd)
            sys.path = old_sys_path
    
    return proxy_app


def wsgi_app(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    
    if path == '/api/logs':
        query = environ.get('QUERY_STRING', '')
        offset = 0
        if 'offset=' in query:
            try:
                offset = int(query.split('offset=')[1].split('&')[0])
            except:
                pass
        
        logs, next_offset = terminal_logs.get_logs(offset)
        
        response_body = json.dumps({
            "logs": logs,
            "next_offset": next_offset
        }).encode('utf-8')
        
        start_response('200 OK', [
            ('Content-Type', 'application/json; charset=utf-8'),
            ('Access-Control-Allow-Origin', '*')
        ])
        return [response_body]

    # --- API KÍCH HOẠT AI SERVER TỪ XA ---
    if path == '/api/start-ai-server' and method == 'POST':
        try:
            print(f"   {Colors.YELLOW}⚡ Đang nhận lệnh bật AI ChatBox Server...{Colors.RESET}")
            
            # Khởi động Server B ngầm qua môi trường ảo myenv
            cmd = "~/myenv/bin/python3 /sdcard/coder/media/Ai-ChatBox/server.py"
            subprocess.Popen(
                cmd,
                shell=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setsid # Giúp tách luồng, Server A tắt thì Server B vẫn sống
            )
            
            response_body = json.dumps({
                "status": "success", 
                "message": "Đã gửi lệnh khởi động AI Server thành công!"
            }).encode('utf-8')
            
            start_response('200 OK', [
                ('Content-Type', 'application/json; charset=utf-8'),
                ('Access-Control-Allow-Origin', '*')
            ])
            return [response_body]
            
        except Exception as e:
            print(f"   {Colors.RED}❌ Lỗi bật AI Server: {str(e)}{Colors.RESET}")
            response_body = json.dumps({
                "status": "error", 
                "message": str(e)
            }).encode('utf-8')
            
            start_response('500 Internal Server Error', [
                ('Content-Type', 'application/json; charset=utf-8'),
                ('Access-Control-Allow-Origin', '*')
            ])
            return [response_body]
    # -------------------------------------

    # --- API TẮT AI SERVER TỪ XA ---
    if path == '/api/stop-ai-server' and method == 'POST':
        try:
            print(f"   {Colors.YELLOW}⚡ Nhận lệnh tắt AI Server. Đang gửi tín hiệu tới port 25152...{Colors.RESET}")

            # Gửi request shutdown tới AI Server (port 25152) một cách an toàn
            shutdown_url = "http://127.0.0.1:25152/api/shutdown"
            requests.post(shutdown_url, timeout=3)

            response_body = json.dumps({
                "status": "success", 
                "message": "Đã gửi lệnh tắt thành công tới AI Server (Port 25152)!"
            }).encode('utf-8')
            
            start_response('200 OK', [
                ('Content-Type', 'application/json; charset=utf-8'),
                ('Access-Control-Allow-Origin', '*')
            ])
            return [response_body]

        except requests.exceptions.RequestException as e:
            # Lỗi này thường xảy ra nếu AI server đã tắt rồi, nên ta vẫn coi là thành công.
            print(f"   {Colors.YELLOW}⚠️  Không thể kết nối tới AI Server để tắt (có thể đã tắt sẵn): {str(e)}{Colors.RESET}")
            response_body = json.dumps({
                "status": "success", 
                "message": "Không thể kết nối tới AI Server (có thể đã được tắt trước đó)."
            }).encode('utf-8')
            
            start_response('200 OK', [
                ('Content-Type', 'application/json; charset=utf-8'),
                ('Access-Control-Allow-Origin', '*')
            ])
            return [response_body]

        except Exception as e:
            print(f"   {Colors.RED}❌ Lỗi hệ thống khi gửi lệnh tắt AI Server: {str(e)}{Colors.RESET}")
            response_body = json.dumps({
                "status": "error", 
                "message": str(e)
            }).encode('utf-8')
            
            start_response('500 Internal Server Error', [
                ('Content-Type', 'application/json; charset=utf-8'),
                ('Access-Control-Allow-Origin', '*')
            ])
            return [response_body]

    # -------------------------------------

    if path == '/' or path == '':
        if os.path.exists('index.py'):
            return handle_python_file('index.py', environ, start_response, '')
        elif os.path.exists('index.html'):
            return serve_static_file('index.html', start_response)
        else:
            start_response('404 Not Found', [('Content-type', 'text/plain')])
            return [b'No index.py or index.html found']
    
    path_parts = [p for p in path.strip('/').split('/') if p]
    if not path_parts:
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return [b'Page not found']
    
    folder_name = path_parts[0]
    
    if folder_name.lower() == PHPMYADMIN_DIR_NAME.lower():
        start_response('403 Forbidden', [('Content-type', 'text/html; charset=utf-8')])
        return [f'<h2>Vui lòng truy cập phpMyAdmin qua cổng {PHPMYADMIN_PORT}</h2><p>Sử dụng link: <a href="http://localhost:{PHPMYADMIN_PORT}">http://localhost:{PHPMYADMIN_PORT}</a></p>'.encode('utf-8')]

    remaining = path_parts[1:]
    
    if os.path.isdir(folder_name):
        if remaining:
            file_path = os.path.normpath(os.path.join(folder_name, *remaining))
            if os.path.exists(file_path) and os.path.isfile(file_path):
                if file_path.endswith('.py'):
                    base_path = '/' + os.path.dirname(file_path)
                    return handle_python_file(file_path, environ, start_response, base_path)
                else:
                    return serve_static_file(file_path, start_response)
            else:
                start_response('404 Not Found', [('Content-type', 'text/plain')])
                return [f'File not found: {file_path}'.encode('utf-8')]
        else:
            public_index = os.path.join(folder_name, 'public', 'index.py')
            index_py = os.path.join(folder_name, 'index.py')
            index_html = os.path.join(folder_name, 'index.html')
            base_path = '/' + folder_name
            
            if os.path.exists(public_index):
                return handle_python_file(public_index, environ, start_response, base_path)
            elif os.path.exists(index_py):
                return handle_python_file(index_py, environ, start_response, base_path)
            elif os.path.exists(index_html):
                return serve_static_file(index_html, start_response)
            else:
                start_response('404 Not Found', [('Content-type', 'text/plain')])
                return [f'No index file in {folder_name}'.encode('utf-8')]
    else:
        check_path = path.strip('/')
        if os.path.isfile(check_path):
            if check_path.endswith('.py'):
                return handle_python_file(check_path, environ, start_response, '')
            else:
                return serve_static_file(check_path, start_response)
        
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return [f'Not found: {folder_name}'.encode('utf-8')]


def handle_python_file(file_path, environ, start_response, base_path):
    result = load_flask_app_from_py(file_path)
    
    if result is not None:
        flask_app, script_dir = result
        proxy = create_flask_proxy(flask_app, script_dir, base_path)
        new_environ = environ.copy()
        original_path = environ.get('PATH_INFO', '/')
        
        if base_path and original_path.startswith(base_path):
            new_environ['PATH_INFO'] = original_path[len(base_path):]
            if not new_environ['PATH_INFO']:
                new_environ['PATH_INFO'] = '/'
        
        return proxy(new_environ, start_response)
    
    try:
        script_dir = os.path.dirname(os.path.abspath(file_path)) or '.'
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=script_dir
        )
        output = result.stdout
        if result.stderr:
            output += "\n\nERROR:\n" + result.stderr
        
        start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])
        return [output.encode('utf-8')]
    except Exception as e:
        start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
        return [f'Error: {str(e)}'.encode('utf-8')]


def serve_static_file(file_path, start_response):
    try:
        if not os.path.isabs(file_path):
            file_path = os.path.normpath(os.path.join(BASE_DIR, file_path))
        
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        
        with open(file_path, 'rb') as f:
            content = f.read()
        
        start_response('200 OK', [('Content-Type', mime_type)])
        return [content]
    except Exception as e:
        start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
        return [f'Error: {str(e)}'.encode('utf-8')]


# --- QUẢN LÝ PHPMYADMIN (MỚI) ---
def start_phpmyadmin():
    global php_process
    pma_path = os.path.join(BASE_DIR, PHPMYADMIN_DIR_NAME)
    
    if not os.path.exists(pma_path):
        print(f"   {Colors.YELLOW}⚠️  Chưa tìm thấy phpMyAdmin!{Colors.RESET}")
        print(f"   {Colors.GRAY}👉 Vị trí yêu cầu: {pma_path}{Colors.RESET}")
        print(f"   {Colors.GRAY}👉 Vui lòng chép thư mục phpMyAdmin vào thư mục chứa server.{Colors.RESET}")
        return False
        
    print(f"   {Colors.GRAY}🔄  Đang nạp database UI (phpMyAdmin)...{Colors.RESET}")
    cmd = ["php", "-S", f"0.0.0.0:{PHPMYADMIN_PORT}", "-t", pma_path]
    
    try:
        php_process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        import time
        time.sleep(0.5)
        if php_process.poll() is not None:
            _, err = php_process.communicate()
            print(f"   {Colors.RED}❌ phpMyAdmin không thể khởi động:{Colors.RESET}")
            print(f"   {Colors.RED}Chi tiết lỗi: {err.strip()}{Colors.RESET}")
            return False
            
        return True
    except FileNotFoundError:
        print(f"   {Colors.RED}❌ Lỗi: Hệ thống Ubuntu chưa có PHP. Hãy chạy lệnh: apt install php{Colors.RESET}")
        return False
    except Exception as e:
        print(f"   {Colors.RED}❌ Lỗi khởi động phpMyAdmin: {e}{Colors.RESET}")
        return False


def start_cloudflared():
    global tunnel_process
    if not os.path.exists(CLOUDFLARE_BIN):
        print(f"   {Colors.YELLOW}⚠️  Cloudflare Tunnel không tìm thấy{Colors.RESET}")
        return
    
    print(f"   {Colors.GRAY}🔄  Đang khởi động Cloudflare Tunnel...{Colors.RESET}")
    cmd = [CLOUDFLARE_BIN, "tunnel", "--url", f"http://localhost:{PORT}"]
    
    try:
        tunnel_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except PermissionError:
        print(f"   {Colors.RED}❌ Chạy: chmod +x $HOME/cloudflared-linux-arm64{Colors.RESET}")
        return
    
    def read_stream():
        url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")
        found = False
        while True:
            if tunnel_process.poll() is not None:
                break
            line = tunnel_process.stderr.readline()
            if not line:
                break
            if not found:
                match = url_pattern.search(line)
                if match:
                    print(f"\n   {Colors.GREEN}🌍  PUBLIC URL: {Colors.CYAN}{Colors.UNDERLINE}{match.group(0)}{Colors.RESET}\n")
                    found = True
    
    threading.Thread(target=read_stream, daemon=True).start()


def cleanup():
    global tunnel_process, php_process
    if tunnel_process:
        tunnel_process.terminate()
    if php_process:
        php_process.terminate()

atexit.register(cleanup)


def get_local_ip():
    try:
        result = subprocess.run(['ifconfig'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'inet ' in line and '127.' not in line:
                parts = line.split()
                for i, p in enumerate(parts):
                    if p == 'inet' and i+1 < len(parts):
                        return parts[i+1]
    except:
        pass
    return "127.0.0.1"


def scan_projects():
    projects = []
    for item in os.listdir(BASE_DIR):
        item_path = os.path.join(BASE_DIR, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            
            if item.lower() == PHPMYADMIN_DIR_NAME.lower():
                projects.append({'name': item, 'type': f"{Colors.MAGENTA}Database UI (PHP){Colors.RESET}"})
                continue
                
            has_public = os.path.isdir(os.path.join(item_path, 'public')) and \
                         os.path.exists(os.path.join(item_path, 'public', 'index.py'))
            has_index_py = os.path.exists(os.path.join(item_path, 'index.py'))
            has_index_html = os.path.exists(os.path.join(item_path, 'index.html'))
            
            if has_public or has_index_py or has_index_html:
                ptype = []
                if has_public:
                    ptype.append(f"{Colors.GREEN}Flask{Colors.RESET}")
                elif has_index_py:
                    ptype.append(f"{Colors.YELLOW}Python{Colors.RESET}")
                if has_index_html:
                    ptype.append(f"{Colors.CYAN}HTML{Colors.RESET}")
                projects.append({'name': item, 'type': ' | '.join(ptype)})
    return projects


class AppRequestHandler(WSGIRequestHandler):
    def log_message(self, format, *args):
        try:
            req_line = args[0]
            status = str(args[1])
            size = str(args[2]) if len(args) > 2 else "-"
            
            parts = req_line.split()
            method = parts[0] if len(parts) > 0 else "REQ"
            path = parts[1] if len(parts) > 1 else req_line

            if path.startswith('/api/logs'):
                return

            method_color = Colors.CYAN
            if method == 'GET': method_color = Colors.BLUE
            elif method == 'POST': method_color = Colors.GREEN
            elif method in ('PUT', 'PATCH'): method_color = Colors.YELLOW
            elif method == 'DELETE': method_color = Colors.RED

            status_color = Colors.GREEN
            if status.startswith('3'): status_color = Colors.YELLOW
            elif status.startswith('4'): status_color = Colors.RED
            elif status.startswith('5'): status_color = Colors.MAGENTA

            import time
            current_time = time.strftime("%H:%M:%S")
            
            print(f"   {Colors.GRAY}[{current_time}]{Colors.RESET} {method_color}{method.ljust(7)}{Colors.RESET} {path} {Colors.GRAY}→{Colors.RESET} {status_color}{status}{Colors.RESET} {Colors.DIM}({size} B){Colors.RESET}")
        except Exception:
            pass

    def handle(self):
        try:
            super().handle()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass


def run_server():
    print("\033[H\033[J", end="")
    
    print(f"\n{Colors.CYAN}   ╭──────────────────────────────────────────────────────╮{Colors.RESET}")
    print(f"{Colors.CYAN}   │ {Colors.WHITE}{Colors.BOLD}🚀  MULTI-PROJECT SERVER{Colors.RESET}                             {Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}   │ {Colors.GRAY}    Quản lý và chạy các dự án web local              {Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}   ╰──────────────────────────────────────────────────────╯{Colors.RESET}\n")
    
    pma_started = start_phpmyadmin()
    start_cloudflared()
    
    local_ip = get_local_ip()
    projects = scan_projects()
    
    print(f"   {Colors.BOLD}📡  THÔNG TIN KẾT NỐI{Colors.RESET}")
    print(f"   {Colors.GRAY}──────────────────────────────────────────────────────{Colors.RESET}")
    print(f"   🏠  Main Server ({PORT}):  {Colors.GREEN}http://localhost:{PORT}{Colors.RESET}")
    print(f"   �  Network IP:          {Colors.GREEN}http://{local_ip}:{PORT}{Colors.RESET}")
    if pma_started:
        print(f"   🗄️   phpMyAdmin (1212):   {Colors.MAGENTA}http://localhost:{PHPMYADMIN_PORT}{Colors.RESET}")
    print(f"   {Colors.GRAY}──────────────────────────────────────────────────────{Colors.RESET}\n")
    
    print(f"   {Colors.GREEN}✅  Server đang hoạt động ổn định...{Colors.RESET}")
    print(f"   {Colors.YELLOW}⚠️   Nhấn Ctrl+C để dừng tất cả Server{Colors.RESET}\n")
    
    try:
        httpd = make_server('0.0.0.0', PORT, wsgi_app, handler_class=AppRequestHandler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n   {Colors.RED}🛑  Đang dọn dẹp và tắt toàn bộ Server...{Colors.RESET}\n")
        sys.exit(0)


if __name__ == "__main__":
    run_server()