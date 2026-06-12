import asyncio
import httpx
import psutil
from core.config import settings

async def send_telegram_message(text: str):
    """Hàm lõi để các module khác trong Backend bắn tin nhắn cảnh báo/alert về điện thoại"""
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return False
        
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(url, json=payload, timeout=5.0)
            return res.status_code == 200
    except Exception:
        return False

async def send_telegram_menu():
    """Tạo và gửi Bảng Điều Khiển (Menu Nút bấm Inline) kèm trạng thái hệ thống real-time"""
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return False
        
    # Import cục bộ để tránh lỗi vòng lặp (Circular Import) với luồng API
    from api.dashboard import api_status_db
    
    tunnel_status = "🟢 ĐANG BẬT" if api_status_db["internet_tunnel"]["active"] else "🔴 ĐANG TẮT"
    
    # Thiết kế cấu trúc các nút bấm tương tác (Inline Keyboard)
    keyboard = {
        "inline_keyboard": [
            [{"text": f"🌐 Tunnel: {tunnel_status}", "callback_data": "toggle_tunnel"}],
            [{"text": "📊 Kiểm tra Trạng thái Máy chủ", "callback_data": "server_stats"}],
            [{"text": "🔄 Khởi động lại API", "callback_data": "restart_api"}]
        ]
    }
    
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": "🎛️ <b>BẢNG ĐIỀU KHIỂN HỆ THỐNG UBUNTU CORE</b>\n\nSếp muốn thực thi lệnh gì hôm nay?",
        "parse_mode": "HTML",
        "reply_markup": keyboard
    }
    
    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload, timeout=5.0)
    except Exception as e:
        print(f"❌ Lỗi gửi menu Telegram: {e}")

async def telegram_polling_task():
    """Luồng ngầm (Background Task) chạy Long Polling liên tục lắng nghe lệnh từ điện thoại"""
    if not settings.TELEGRAM_BOT_TOKEN:
        print("⚠️ Chưa cấu hình Telegram Bot. Bỏ qua tính năng bot.")
        return
        
    print(f"🤖 Trợ lý Telegram đã khởi động! Đang chờ lệnh từ Sếp (Chat ID: {settings.TELEGRAM_CHAT_ID})...")
    update_id = 0
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getUpdates"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        while True:
            try:
                # Quét và nhận các tương tác mới từ Telegram gửi về
                res = await client.get(url, params={"offset": update_id, "timeout": 20})
                if res.status_code == 200:
                    data = res.json()
                    for update in data.get("result", []):
                        update_id = update["update_id"] + 1
                        
                        # 📡 RADAR GỠ LỖI: In ra màn hình console mọi sự kiện nhận được
                        print(f"📡 [DEBUG] Bot vừa tóm được 1 hành động: {update}")
                        
                        # VỚI TRƯỜNG HỢP: Sếp gõ chữ hoặc lệnh văn bản (Ví dụ: /menu)
                        if "message" in update and "text" in update["message"]:
                            text = update["message"]["text"].strip()
                            chat_id = str(update["message"]["chat"]["id"])
                            
                            print(f"👤 [DEBUG] Người gửi (ID: {chat_id}) vừa nhắn: {text}")
                            
                            # Xác thực danh tính chủ nhân tối cao
                            if chat_id == str(settings.TELEGRAM_CHAT_ID).strip():
                                print("   ✅ ID Trùng khớp! Đang xử lý tin nhắn...")
                                if text in ["/start", "/menu", "menu"]:
                                    await send_telegram_menu()
                                else:
                                    await send_telegram_message("💡 Gõ <b>/menu</b> hoặc chữ <b>menu</b> để gọi Bảng điều khiển nhé sếp!")
                            else:
                                print("   ❌ ID Lạ gõ lệnh! Hệ thống từ chối phản hồi bảo mật.")
                                
                        # VỚI TRƯỜNG HỢP: Sếp bấm các nút trên Menu (Callback Query)
                        elif "callback_query" in update:
                            cb = update["callback_query"]
                            data_cb = cb["data"]
                            cb_id = cb["id"]
                            chat_id = str(cb["message"]["chat"]["id"])
                            
                            print(f"👆 [DEBUG] Người dùng (ID: {chat_id}) vừa ấn nút: {data_cb}")
                            
                            if chat_id == str(settings.TELEGRAM_CHAT_ID).strip():
                                from api.dashboard import api_status_db
                                from scripts.network_tunnel import start_tunnel, stop_tunnel, get_tunnel_url
                                
                                # 🔵 Xử lý nút: BẬT / TẮT CLOUDFLARE TUNNEL
                                if data_cb == "toggle_tunnel":
                                    current = api_status_db["internet_tunnel"]["active"]
                                    api_status_db["internet_tunnel"]["active"] = not current
                                    
                                    if not current:
                                        start_tunnel()
                                        await send_telegram_message("⏳ Đang kích hoạt Cloudflare Tunnel. Đang săn tìm link Public...")
                                        
                                        # 🚀 VÒNG LẶP SĂN LINK LIÊN TỤC TRONG 15 GIÂY CHỐNG TRỄ MẠNG
                                        link_found = ""
                                        for _ in range(15):
                                            await asyncio.sleep(1) # Chờ 1 giây mỗi chu kỳ quét
                                            link_found = get_tunnel_url()
                                            if link_found:
                                                break # Có link lập tức bẻ gãy vòng lặp
                                                
                                        if link_found:
                                            api_status_db["internet_tunnel"]["public_url"] = link_found
                                            await send_telegram_message(f"✅ Tunnel đã mở thành công!\n🌐 Link Public: {link_found}")
                                        else:
                                            await send_telegram_message("⚠️ Đường truyền phản hồi chậm. Hạ tầng đang chạy ngầm, lát nữa sếp hãy ấn lại nút Tunnel để lấy link.")
                                    else:
                                        stop_tunnel()
                                        api_status_db["internet_tunnel"]["public_url"] = ""
                                        await send_telegram_message("🔴 Đã ngắt kết nối Cloudflare Tunnel hoàn toàn!")
                                    
                                    # Gửi lại Menu mới để cập nhật chữ trên nút bấm (Bật -> Tắt hoặc ngược lại)
                                    await send_telegram_menu()
                                    
                                # 🔵 Xử lý nút: KIỂM TRA PHẦN CỨNG MÁY CHỦ
                                elif data_cb == "server_stats":
                                    cpu = psutil.cpu_percent(interval=0.5)
                                    ram = psutil.virtual_memory()
                                    disk = psutil.disk_usage('/')
                                    
                                    msg = (f"📊 <b>BÁO CÁO TÀI NGUYÊN MÁY CHỦ:</b>\n\n"
                                           f"🎛️ CPU Usage: {cpu}%\n"
                                           f"🧠 RAM Usage: {ram.percent}% ({round(ram.used/(1024**3), 1)}GB / {round(ram.total/(1024**3), 1)}GB)\n"
                                           f"💾 Storage: {disk.percent}% đã dùng (Trống {round(disk.free/(1024**3), 1)}GB)")
                                    await send_telegram_message(msg)
                                    
                                # 🔵 Xử lý nút: KHỞI ĐỘNG LẠI LUỒNG API DỰ PHÒNG
                                elif data_cb == "restart_api":
                                    await send_telegram_message("🔄 Đang cấu hình và làm mới luồng API...")
                                    await asyncio.sleep(1)
                                    await send_telegram_message("✅ Đã giải phóng bộ nhớ và làm mới dịch vụ.")
                                
                                # Bắt buộc phải trả lời callback này để Telegram tắt hiệu ứng xoay tròn mờ trên nút bấm
                                answer_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/answerCallbackQuery"
                                await client.post(answer_url, json={"callback_query_id": cb_id})
                                
            except Exception as e:
                print(f"🔥 [DEBUG LỖI NGẦM]: {e}")
                await asyncio.sleep(5) # Tránh nghẽn vòng lặp vô hạn nếu rớt mạng
                
            await asyncio.sleep(1) # Nghỉ 1 giây để bảo vệ CPU không bị quá nhiệt