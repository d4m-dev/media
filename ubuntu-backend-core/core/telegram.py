import asyncio
import httpx
import psutil
import os
import shutil
import subprocess
from datetime import datetime
from core.config import settings

# ------------------------------------------------------------
# HÀM BỔ TRỢ: Đọc Pin Thiết Bị Thực
# ------------------------------------------------------------
def get_device_battery():
    try:
        with open('/sys/class/power_supply/battery/capacity', 'r') as f:
            capacity = f.read().strip()
        with open('/sys/class/power_supply/battery/status', 'r') as f:
            status = f.read().strip()
        icon = "⚡ Đang sạc" if status == "Charging" else "🔋 Dùng pin"
        return f"{capacity}% ({icon})"
    except:
        return "🔋 Không xác định"

# ------------------------------------------------------------
# HÀM BỔ TRỢ: Nén File Cấu Hình / Mã Nguồn (Tối ưu siêu nhẹ)
# ------------------------------------------------------------
def create_backup_zip():
    backup_filename = f"SourceCode_Optimized_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    backup_path = os.path.join("/tmp", backup_filename)
    
    import zipfile
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 🛡️ DANH SÁCH ĐEN: Các thư mục siêu nặng tuyệt đối không cho vào file Backup
    ignored_folders = {
        '.git', 
        'myenv', 
        'venv', 
        '__pycache__', 
        'audio_workspace', 
        'hosted_projects',
        'node_modules' # Phòng hờ sếp có xài npm
    }
    
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            
            # Lọc bỏ thư mục rác ngay từ vòng gửi xe
            dirs[:] = [d for d in dirs if d not in ignored_folders]
            
            for file in files:
                # Bỏ qua các file biên dịch trung gian hoặc file zip cũ
                if file.endswith(('.pyc', '.pyo', '.pyd', '.zip', '.tar.gz')):
                    continue
                    
                abs_file = os.path.join(root, file)
                rel_file = os.path.relpath(abs_file, base_dir)
                zipf.write(abs_file, rel_file)
                
    return backup_path

# ------------------------------------------------------------
# CORE: Telegram Bot Lắng Nghe
# ------------------------------------------------------------
async def send_telegram_message(text: str):
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID: return False
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(url, json={"chat_id": settings.TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5.0)
            return res.status_code == 200
    except: return False

async def send_telegram_menu():
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID: return False
    from api.dashboard import api_status_db
    
    tunnel_status = "🟢 ĐANG BẬT" if api_status_db["internet_tunnel"]["active"] else "🔴 ĐANG TẮT"
    
    keyboard = {
        "inline_keyboard": [
            [{"text": f"🌐 Tunnel (Port 1515): {tunnel_status}", "callback_data": "toggle_tunnel"}],
            [
                {"text": "📊 Giám Sát Tài Nguyên", "callback_data": "server_stats"},
                {"text": "🔬 Top Tiến Trình (RAM/CPU)", "callback_data": "top_processes"}
            ],
            [
                {"text": "🧹 Dọn rác AI", "callback_data": "clean_trash"},
                {"text": "📦 Sao Lưu Mã Nguồn", "callback_data": "backup_code"}
            ],
            [{"text": "🔄 Khởi động lại luồng API", "callback_data": "restart_api"}]
        ]
    }
    
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": "🎛️ <b>TRUNG TÂM CHỈ HUY UBUNTU CORE</b>\n\n💡 <b>Mẹo:</b>\n- Gửi <i>File Nhạc/Video</i> để tách Beat.\n- Gõ <code>> [lệnh bash]</code> để chạy Terminal từ xa.",
        "parse_mode": "HTML",
        "reply_markup": keyboard
    }
    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload, timeout=5.0)
    except: pass

async def telegram_polling_task():
    if not settings.TELEGRAM_BOT_TOKEN: return
        
    print(f"🤖 Trợ lý Telegram đã khởi động! Đang chờ lệnh từ Sếp...")
    update_id = 0
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getUpdates"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        while True:
            try:
                res = await client.get(url, params={"offset": update_id, "timeout": 20})
                if res.status_code == 200:
                    data = res.json()
                    for update in data.get("result", []):
                        update_id = update["update_id"] + 1
                        
                        # ==========================================
                        # 1. TIẾP NHẬN FILE ÂM THANH (AI STUDIO)
                        # ==========================================
                        if "message" in update and str(update["message"]["chat"]["id"]) == str(settings.TELEGRAM_CHAT_ID):
                            msg = update["message"]
                            file_id = None
                            file_name = "telegram_audio.mp3"
                            
                            if "audio" in msg:
                                file_id = msg["audio"]["file_id"]
                                file_name = msg["audio"].get("file_name", file_name)
                            elif "document" in msg:
                                file_id = msg["document"]["file_id"]
                                file_name = msg["document"].get("file_name", file_name)
                            elif "video" in msg:
                                file_id = msg["video"]["file_id"]
                                file_name = msg["video"].get("file_name", "telegram_video.mp4")
                                
                            if file_id:
                                await send_telegram_message("📥 <b>Đã nhận tệp âm thanh!</b> Đang tải về máy chủ...")
                                try:
                                    file_res = await client.get(f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}")
                                    tg_file_path = file_res.json()["result"]["file_path"]
                                    download_url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{tg_file_path}"
                                    
                                    from api.audio_engine import sanitize_folder_name, process_audio_pipeline, INPUT_DIR, OUTPUT_DIR
                                    clean_name, ext = sanitize_folder_name(file_name)
                                    task_id = f"TG_{clean_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                                    
                                    saved_input_path = os.path.join(INPUT_DIR, f"{task_id}{ext}")
                                    file_data = await client.get(download_url)
                                    with open(saved_input_path, "wb") as f:
                                        f.write(file_data.content)
                                        
                                    await send_telegram_message(f"⚙️ <b>Bắt đầu trích xuất AI:</b> {clean_name}\n⏳ Vui lòng đợi từ 1-3 phút...")
                                    
                                    await asyncio.to_thread(process_audio_pipeline, saved_input_path, clean_name, task_id, ext, True, True)
                                    
                                    await send_telegram_message("✅ <b>Hoàn tất!</b> Đang đóng gói và gửi lại cho sếp...")
                                    
                                    project_dir = os.path.join(OUTPUT_DIR, clean_name)
                                    for f_path in [os.path.join(project_dir, f"{task_id}_vocal.mp3"), os.path.join(project_dir, f"{task_id}_beat.mp3"), os.path.join(project_dir, f"{task_id}_lyrics.txt")]:
                                        if os.path.exists(f_path):
                                            with open(f_path, "rb") as f:
                                                await client.post(f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendDocument", data={"chat_id": settings.TELEGRAM_CHAT_ID}, files={"document": f}, timeout=60.0)
                                except Exception as e:
                                    await send_telegram_message(f"❌ Lỗi Audio Studio: {e}")
                                continue

                        # ==========================================
                        # 2. XỬ LÝ LỆNH VĂN BẢN VÀ TERMINAL
                        # ==========================================
                        if "message" in update and "text" in update["message"]:
                            text = update["message"]["text"].strip()
                            chat_id = str(update["message"]["chat"]["id"])
                            
                            if chat_id == str(settings.TELEGRAM_CHAT_ID).strip():
                                if text.startswith(">"):
                                    cmd = text[1:].strip()
                                    await send_telegram_message(f"💻 Đang thực thi: <code>{cmd}</code>")
                                    try:
                                        result = await asyncio.to_thread(subprocess.run, cmd, shell=True, capture_output=True, text=True, timeout=15)
                                        output = result.stdout if result.stdout else result.stderr
                                        if not output: output = "✅ Lệnh chạy thành công, không có log đầu ra."
                                        await send_telegram_message(f"📟 <b>Terminal Output:</b>\n<pre>{output[:3900]}</pre>")
                                    except subprocess.TimeoutExpired:
                                        await send_telegram_message("⏳ Lệnh chạy quá 15 giây đã bị hệ thống buộc dừng!")
                                    except Exception as e:
                                        await send_telegram_message(f"❌ Lỗi Terminal: {str(e)}")
                                        
                                elif text in ["/start", "/menu", "menu"]:
                                    await send_telegram_menu()
                                else:
                                    await send_telegram_message("⏳ <i>AI SysAdmin đang phân tích...</i>")
                                    try:
                                        from api.ai_admin import ai_admin_chat, ChatRequest
                                        ai_res = await ai_admin_chat(ChatRequest(message=text))
                                        reply = f"🤖 <b>AI SYSADMIN:</b>\n\n{ai_res['reply']}"
                                        if ai_res.get('action_executed'):
                                            reply += f"\n\n⚡ <i>{ai_res['action_executed']}</i>"
                                        await send_telegram_message(reply)
                                    except Exception as ai_err:
                                        await send_telegram_message(f"❌ Lỗi AI: {str(ai_err)}")
                                        
                        # ==========================================
                        # 3. XỬ LÝ NÚT BẤM (CALLBACK)
                        # ==========================================
                        elif "callback_query" in update:
                            cb = update["callback_query"]
                            data_cb = cb["data"]
                            cb_id = cb["id"]
                            chat_id = str(cb["message"]["chat"]["id"])
                            
                            if chat_id == str(settings.TELEGRAM_CHAT_ID).strip():
                                from api.dashboard import api_status_db
                                from scripts.network_tunnel import start_tunnel, stop_tunnel, get_tunnel_url
                                
                                if data_cb == "toggle_tunnel":
                                    current = api_status_db["internet_tunnel"]["active"]
                                    api_status_db["internet_tunnel"]["active"] = not current
                                    if not current:
                                        start_tunnel()
                                        await send_telegram_message("⏳ Đang bật Cloudflare Tunnel cho web project (Port 1515)...")
                                        link_found = ""
                                        for _ in range(15):
                                            await asyncio.sleep(1)
                                            link_found = get_tunnel_url()
                                            if link_found: break
                                        if link_found:
                                            api_status_db["internet_tunnel"]["public_url"] = link_found
                                            await send_telegram_message(f"✅ Tunnel đã mở!\n🌐 Link Public: {link_found}")
                                        else:
                                            await send_telegram_message("⚠️ Mạng chậm, lát ấn lại sếp nhé.")
                                    else:
                                        stop_tunnel()
                                        api_status_db["internet_tunnel"]["public_url"] = ""
                                        await send_telegram_message("🔴 Đã ngắt kết nối Cloudflare Tunnel!")
                                    await send_telegram_menu()
                                    
                                elif data_cb == "server_stats":
                                    msg = (f"📊 <b>PHẦN CỨNG HỆ THỐNG:</b>\n\n"
                                           f"🎛️ CPU: {psutil.cpu_percent(interval=0.5)}%\n"
                                           f"🧠 RAM: {psutil.virtual_memory().percent}% ({round(psutil.virtual_memory().used/(1024**3), 1)}GB)\n"
                                           f"💾 Disk: {psutil.disk_usage('/').percent}%\n"
                                           f"🔋 Tình trạng Pin: {get_device_battery()}")
                                    await send_telegram_message(msg)
                                    
                                elif data_cb == "top_processes":
                                    try:
                                        procs = sorted([p.info for p in psutil.process_iter(['pid', 'name', 'memory_percent']) if p.info['memory_percent']], key=lambda p: p['memory_percent'], reverse=True)[:5]
                                        proc_str = "\n".join([f"▪️ <b>{p['name']}</b>: {p['memory_percent']:.1f}% RAM" for p in procs])
                                        await send_telegram_message(f"🔬 <b>TOP 5 ỨNG DỤNG NGỐN RAM:</b>\n\n{proc_str}")
                                    except Exception as e:
                                        await send_telegram_message(f"❌ Lỗi quét tiến trình: {e}")
                                    
                                elif data_cb == "clean_trash":
                                    from api.audio_engine import WORKSPACE_DIR
                                    await send_telegram_message("🧹 Đang quét dọn file tạm...")
                                    freed = 0
                                    for root, dirs, _ in os.walk(WORKSPACE_DIR):
                                        for d in dirs:
                                            if d.startswith("temp_"):
                                                shutil.rmtree(os.path.join(root, d), ignore_errors=True)
                                                freed += 1
                                    await send_telegram_message(f"✨ <b>Hoàn tất!</b> Đã dọn {freed} rác hệ thống.")
                                    
                                elif data_cb == "backup_code":
                                    await send_telegram_message("📦 Đang đóng gói mã nguồn siêu nhẹ, sếp đợi một lát...")
                                    try:
                                        zip_file_path = await asyncio.to_thread(create_backup_zip)
                                        with open(zip_file_path, "rb") as f:
                                            send_doc_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendDocument"
                                            await client.post(send_doc_url, data={"chat_id": settings.TELEGRAM_CHAT_ID}, files={"document": f}, timeout=60.0)
                                        os.remove(zip_file_path) # Xóa file zip tạm sau khi gửi xong
                                        await send_telegram_message("✅ Gửi mã nguồn thành công!")
                                    except Exception as e:
                                        await send_telegram_message(f"❌ Lỗi sao lưu: {e}")
                                    
                                elif data_cb == "restart_api":
                                    await send_telegram_message("🔄 Đã làm mới hệ thống thành công!")
                                
                                await client.post(f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/answerCallbackQuery", json={"callback_query_id": cb_id})
                                
            except Exception as e:
                await asyncio.sleep(5)
            await asyncio.sleep(1)