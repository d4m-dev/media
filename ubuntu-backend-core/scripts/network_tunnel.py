import subprocess
import os
import signal
import time
import re
import urllib.request
import urllib.parse
from core.config import settings

PID_FILE = "/storage/emulated/0/coder/media/ubuntu-backend-core/core/.tunnel.pid"
LOG_FILE = "/storage/emulated/0/coder/media/ubuntu-backend-core/core/.tunnel.log"
CLOUDFLARE = os.path.join(os.environ.get('HOME', '.'), "cloudflared-linux-arm64")

def send_telegram_notification(url):
    """Gửi thông báo qua Telegram nếu có cấu hình token"""
    if settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID:
        try:
            msg = f"🚀 Máy chủ Backend Core đã Online!\n🌐 Truy cập ngay tại: {url}"
            api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={settings.TELEGRAM_CHAT_ID}&text={urllib.parse.quote(msg)}"
            urllib.request.urlopen(api_url)
            print("✅ Đã gửi link trực tiếp qua Telegram Bot!")
        except Exception as e:
            print(f"⚠️ Không thể gửi tin nhắn Telegram: {e}")

def get_public_url():
    """Đọc file log của Cloudflare để trích xuất link public"""
    if not os.path.exists(LOG_FILE): 
        return None
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            # Tìm link có dạng https://xxx.trycloudflare.com
            match = re.search(r'(https://[a-zA-Z0-9-]+\.trycloudflare\.com)', content)
            if match:
                return match.group(1)
    except Exception:
        pass
    return None

def start_tunnel():
    """Khởi động Cloudflare và lấy Link"""
    if os.path.exists(PID_FILE):
        url = get_public_url()
        print("🌐 Tunnel đã được bật từ trước.")
        return True, url
        
    if not os.path.exists(CLOUDFLARE):
        print(f"❌ Không tìm thấy file {CLOUDFLARE}. Hãy đảm bảo file đã tải và chạy lệnh 'chmod +x {CLOUDFLARE}'.")
        return False, None
        
    # Reset file log cũ
    with open(LOG_FILE, "w") as f:
        f.write("")
        
    try:
        log_out = open(LOG_FILE, "w")
        # Chạy Cloudflare và trỏ thẳng vào port 16868, ghi log vào file để quét
        process = subprocess.Popen(
            [CLOUDFLARE, "tunnel", "--url", f"http://127.0.0.1:{settings.PORT}"],
            stdout=subprocess.DEVNULL,
            stderr=log_out
        )
        
        with open(PID_FILE, "w") as f:
            f.write(str(process.pid))
            
        print("⏳ Đang khởi tạo đường hầm Cloudflare... Vui lòng đợi 4 giây...")
        time.sleep(4) # Chờ Cloudflare sinh link
        
        url = get_public_url()
        if url:
            print(f"✅ Đã lên sóng Internet! Public URL: {url}")
            send_telegram_notification(url)
        else:
            print("⚠️ Đường hầm đã chạy nhưng chưa kịp trích xuất Link. Bạn có thể xem trên UI sau vài giây.")
            
        return True, url
    except Exception as e:
        print(f"❌ Lỗi khi bật Tunnel: {e}")
        return False, None

def stop_tunnel():
    """Tắt Cloudflare và dọn dẹp log"""
    if not os.path.exists(PID_FILE):
        return True
        
    try:
        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())
        
        os.kill(pid, signal.SIGTERM)
        time.sleep(1) 
        
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
            
        print("🛑 Đã ngắt đường hầm Internet an toàn!")
        return True
    except ProcessLookupError:
        if os.path.exists(PID_FILE): os.remove(PID_FILE)
        return True
    except Exception as e:
        print(f"❌ Lỗi khi tắt Tunnel: {e}")
        return False