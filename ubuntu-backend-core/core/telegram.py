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
        
    # Import cục bộ để tránh lỗi vòng lặp (Circular Import) với luồng khởi động API
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
                        
                        # ==========================================
                        # VỚI TRƯỜNG HỢP: SẾP GÕ CHỮ HOẶC RA LỆNH VĂN BẢN
                        # ==========================================
                        if "message" in update and "text" in update["message"]:
                            text = update["message"]["text"].strip()
                            chat_id = str(update["message"]["chat"]["id"])
                            
                            print(f"👤 [DEBUG] Người gửi (ID: {chat_id}) vừa nhắn: {text}")
                            
                            # Xác thực danh tính chủ nhân tối cao để bảo mật hệ thống
                            if chat_id == str(settings.TELEGRAM_CHAT_ID).strip():
                                print("   ✅ ID Trùng khớp! Đang xử lý...")
                                
                                # Nếu là lệnh menu cơ bản
                                if text in ["/start", "/menu", "menu"]:
                                    await send_telegram_menu()
                                    
                                # Nếu là câu hỏi hoặc lệnh tự nhiên -> Đẩy thẳng vào bộ não AI Gemini
                                else:
                                    await send_telegram_message("⏳ <i>AI SysAdmin đang phân tích yêu cầu của sếp...</i>")
                                    try:
                                        # Gọi module AI xử lý tương tác hạ tầng giống hệt trên Web Dashboard
                                        from api.ai_admin import ai_admin_chat, ChatRequest
                                        ai_req = ChatRequest(message=text)
                                        ai_res = await ai_admin_chat(ai_req)
                                        
                                        # Định dạng câu trả lời của AI gửi lại cho sếp
                                        reply = f"🤖 <b>AI SYSADMIN:</b>\n\n{ai_res['reply']}"
                                        if ai_res.get('action_executed'):
                                            reply += f"\n\n⚡ <i>{ai_res['action_executed']}</i>"
                                            
                                        await send_telegram_message(reply)
                                    except Exception as ai_err:
                                        await send_telegram_message(f"❌ Lỗi xử lý AI: {str(ai_err)}")
                            else:
                                print("   ❌ ID Lạ gõ lệnh! Hệ thống từ chối phản hồi bảo mật.")
                                
                        # ==========================================
                        # VỚI TRƯỜNG HỢP: SẾP BẤM CÁC NÚT TRÊN MENU (CALLBACK)
                        # ==========================================
                        elif "callback_query" in update:
                            cb = update["callback_query"]
                            data_cb = cb["data"]
                            cb_id = cb["id"]
                            chat_id = str(cb["message"]["chat"]["id"])
                            
                            print(f"👆 [DEBUG] Người dùng (ID: {chat_id}) vừa ấn nút: {data_cb}")
                            
                            if chat_id == str(settings.TELEGRAM_CHAT_ID).strip():
                                from api.dashboard import api_status_db
                                from scripts.network_tunnel import start_tunnel, stop_tunnel, get_tunnel_url
                                
                                # 🔵 Xử lý nút: BẬT / TẮT CLOUDFLARE TUNNEL (CỔNG 16868)
                                if data_cb == "toggle_tunnel":
                                    current = api_status_db["internet_tunnel"]["active"]
                                    api_status_db["internet_tunnel"]["active"] = not current
                                    
                                    if not current:
                                        start_tunnel()
                                        await send_telegram_message("⏳ Đang kích hoạt Cloudflare Tunnel. Đang săn tìm link Public...")
                                        
                                        # Vòng lặp săn tìm link public trong 15 giây chống trễ mạng
                                        link_found = ""
                                        for _ in range(15):
                                            await asyncio.sleep(1)
                                            link_found = get_tunnel_url()
                                            if link_found:
                                                break
                                                
                                        if link_found:
                                            api_status_db["internet_tunnel"]["public_url"] = link_found
                                            await send_telegram_message(f"✅ Tunnel đã mở thành công tại port 16868!\n🌐 Link Public: {link_found}")
                                        else:
                                            await send_telegram_message("⚠️ Đường truyền phản hồi chậm. Hạ tầng đang chạy ngầm, lát nữa sếp hãy ấn lại nút Tunnel để lấy link.")
                                    else:
                                        stop_tunnel()
                                        api_status_db["internet_tunnel"]["public_url"] = ""
                                        await send_telegram_message("🔴 Đã ngắt kết nối Cloudflare Tunnel hoàn toàn!")
                                    
                                    await send_telegram_menu()
                                    
                                # 🔵 Xử lý nút: KIỂM TRA PHẦN CỨNG MÁY CHỦ S26 ULTRA
                                elif data_cb == "server_stats":
                                    cpu = psutil.cpu_percent(interval=0.5)
                                    ram = psutil.virtual_memory()
                                    disk = psutil.disk_usage('/')
                                    
                                    msg = (f"📊 <b>BÁO CÁO TÀI NGUYÊN MÁY CHỦ:</b>\n\n"
                                           f"🎛️ CPU Usage: {cpu}%\n"
                                           f"🧠 RAM Usage: {ram.percent}% ({round(ram.used/(1024**3), 1)}GB / {round(ram.total/(1024**3), 1)}GB)\n"
                                           f"💾 Storage: {disk.percent}% đã dùng (Trống {round(disk.free/(1024**3), 1)}GB)")
                                    await send_telegram_message(msg)
                                    
                                # 🔵 Xử lý nút: KHỞI ĐỘNG LẠI LUỒNG API
                                elif data_cb == "restart_api":
                                    await send_telegram_message("🔄 Đang tiến hành dọn dẹp RAM và đồng bộ lại dịch vụ trên cổng 16868...")
                                    await asyncio.sleep(1)
                                    await send_telegram_message("✅ Hệ thống lõi đã được làm mới mượt mà!")
                                
                                # Phản hồi callback để tắt hiệu ứng loading xoay tròn trên nút bấm Telegram
                                answer_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/answerCallbackQuery"
                                await client.post(answer_url, json={"callback_query_id": cb_id})
                                
            except Exception as e:
                print(f"🔥 [DEBUG LỖI NGẦM]: {e}")
                await asyncio.sleep(5) # Tránh nghẽn vô hạn nếu rớt mạng hoàn toàn
                
            await asyncio.sleep(1) # Nghỉ 1 giây bảo vệ thiết bị tránh quá nhiệt CPU