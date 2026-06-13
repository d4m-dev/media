import asyncio
import httpx
import psutil
import os
import shutil
import subprocess
from datetime import datetime
from core.config import settings

# 🚀 BIẾN TOÀN CỤC LƯU TRẠNG THÁI CHỜ 2 BƯỚC CỦA BOT
pending_audio_tasks = {}

# ------------------------------------------------------------
# HÀM BỔ TRỢ: Đọc Pin & Sao Lưu
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

def create_backup_zip():
    backup_filename = f"SourceCode_Optimized_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    backup_path = os.path.join("/tmp", backup_filename)
    import zipfile
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    ignored_folders = {'.git', 'myenv', 'venv', '__pycache__', 'audio_workspace', 'hosted_projects', 'node_modules'}
    
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in ignored_folders]
            for file in files:
                if file.endswith(('.pyc', '.pyo', '.pyd', '.zip', '.tar.gz')): 
                    continue
                abs_file = os.path.join(root, file)
                rel_file = os.path.relpath(abs_file, base_dir)
                zipf.write(abs_file, rel_file)
    return backup_path

# ------------------------------------------------------------
# CORE: Các hàm giao tiếp Telegram
# ------------------------------------------------------------
async def send_telegram_message(text: str, reply_markup: dict = None):
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID: return False
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": settings.TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    if reply_markup: 
        payload["reply_markup"] = reply_markup
    
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(url, json=payload, timeout=5.0)
            return res.status_code == 200
    except: return False

async def send_telegram_menu():
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID: return False
    from api.dashboard import api_status_db
    
    tunnel_status = "🟢 ĐANG BẬT" if api_status_db["internet_tunnel"]["active"] else "🔴 ĐANG TẮT"
    keyboard = {
        "inline_keyboard": [
            [{"text": f"🌐 Tunnel (Cổng 16868): {tunnel_status}", "callback_data": "toggle_tunnel"}],
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
    await send_telegram_message(
        "🎛️ <b>TRUNG TÂM CHỈ HUY UBUNTU CORE</b>\n\n"
        "💡 <b>Mẹo nâng cấp:</b>\n"
        "- Khi gửi file Nhạc/Video, hãy nhập tên bài hát vào phần <b>Chú thích (Caption)</b> để AI tìm đúng lời!\n"
        "- Gõ <code>> [lệnh bash]</code> để chạy Terminal từ xa.", 
        reply_markup=keyboard
    )

# ------------------------------------------------------------
# LUỒNG XỬ LÝ ÂM THANH NGẦM (Theo đúng Option sếp chọn)
# ------------------------------------------------------------
async def trigger_audio_processing(chat_id: str, file_id: str, chosen_name: str, original_filename: str, option: str):
    await send_telegram_message(f"📥 <b>Đang nạp file vào hệ sinh thái riêng:</b> <code>{chosen_name}</code>...")
    
    try:
        async with httpx.AsyncClient() as client:
            file_res = await client.get(f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}")
            tg_file_path = file_res.json()["result"]["file_path"]
            download_url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{tg_file_path}"
            
            from api.audio_engine import sanitize_folder_name, process_audio_pipeline, WORKSPACE_DIR
            
            TELEGRAM_DIR = os.path.join(WORKSPACE_DIR, "telegram")
            os.makedirs(TELEGRAM_DIR, exist_ok=True)
            
            clean_name, _ = sanitize_folder_name(chosen_name)
            _, ext = sanitize_folder_name(original_filename)
            
            task_id = f"{clean_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            project_dir = os.path.join(TELEGRAM_DIR, clean_name)
            os.makedirs(project_dir, exist_ok=True)
            
            saved_input_path = os.path.join(project_dir, f"{task_id}{ext}")
            file_data = await client.get(download_url)
            with open(saved_input_path, "wb") as f:
                f.write(file_data.content)
                
            # 🚀 CẤU HÌNH CỜ BẬT TẮT AI DỰA THEO LỰA CHỌN CỦA SẾP
            separate_beat = option in ["vocal", "beat", "all"]
            extract_lyrics = option in ["lyric", "all"]
            
            await send_telegram_message(f"⚙️ <b>Đang chạy AI trích xuất:</b> {clean_name}\n⏳ Sếp cứ làm việc khác, xong mình gửi kết quả qua nhé!")
            
            # Chạy pipeline theo đúng cờ đã bật
            await asyncio.to_thread(process_audio_pipeline, saved_input_path, clean_name, task_id, ext, separate_beat, extract_lyrics, TELEGRAM_DIR, TELEGRAM_DIR)
            
            await send_telegram_message(f"✅ <b>AI đã làm xong:</b> {clean_name}\n📦 Đang lọc và gửi đúng file sếp yêu cầu...")
            
            # 🚀 CHỈ CHỌN LỌC NHỮNG FILE SẾP YÊU CẦU ĐỂ GỬI TRẢ
            files_to_send = []
            if option in ["vocal", "all"]: files_to_send.append(f"{task_id}_vocal.mp3")
            if option in ["beat", "all"]: files_to_send.append(f"{task_id}_beat.mp3")
            if option in ["lyric", "all"]: files_to_send.append(f"{task_id}_lyrics.lrc")
            
            for f_name in files_to_send:
                f_path = os.path.join(project_dir, f_name)
                if os.path.exists(f_path):
                    with open(f_path, "rb") as f:
                        await client.post(f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendDocument", data={"chat_id": chat_id}, files={"document": f}, timeout=60.0)
    except Exception as e:
        await send_telegram_message(f"❌ Lỗi hạ tầng Audio: {e}")

# ------------------------------------------------------------
# CORE: VÒNG LẶP LẮNG NGHE CHÍNH
# ------------------------------------------------------------
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
                        # 1. TIẾP NHẬN FILE (BƯỚC 1: HỎI TÊN)
                        # ==========================================
                        if "message" in update and str(update["message"]["chat"]["id"]) == str(settings.TELEGRAM_CHAT_ID):
                            msg = update["message"]
                            chat_id = str(msg["chat"]["id"])
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
                                custom_caption = msg.get("caption", "").strip()
                                suggested_name = custom_caption if custom_caption else file_name.split('.')[0]
                                
                                # Đưa vào trạng thái chờ bước 1 (name)
                                pending_audio_tasks[chat_id] = {
                                    "step": "name",
                                    "file_id": file_id,
                                    "original_filename": file_name,
                                    "suggested_name": suggested_name,
                                    "chosen_name": ""
                                }
                                
                                keyboard = {
                                    "inline_keyboard": [
                                        [{"text": f"✅ Dùng tên: {suggested_name}", "callback_data": "confirm_audio_name"}],
                                        [{"text": "❌ Hủy bỏ", "callback_data": "cancel_audio_name"}]
                                    ]
                                }
                                await send_telegram_message(
                                    "📥 <b>Bot đã nhận tệp!</b>\n\nSếp muốn đặt tên dự án là gì?\n✏️ Gõ tin nhắn để <b>nhập tên mới</b>\nHoặc bấm nút để <b>dùng tên mặc định</b>:", 
                                    reply_markup=keyboard
                                )
                                continue

                        # ==========================================
                        # 2. XỬ LÝ LỆNH VĂN BẢN VÀ TERMINAL
                        # ==========================================
                        if "message" in update and "text" in update["message"]:
                            text = update["message"]["text"].strip()
                            chat_id = str(update["message"]["chat"]["id"])
                            
                            if chat_id == str(settings.TELEGRAM_CHAT_ID).strip():
                                
                                # NHẬN TÊN TỪ VĂN BẢN KHI ĐANG Ở BƯỚC 1 (name)
                                if chat_id in pending_audio_tasks and pending_audio_tasks[chat_id].get("step") == "name" and not text.startswith(">") and text not in ["/start", "/menu", "menu"]:
                                    pending_audio_tasks[chat_id]["chosen_name"] = text
                                    pending_audio_tasks[chat_id]["step"] = "option" # Chuyển sang bước 2
                                    
                                    kb_options = {
                                        "inline_keyboard": [
                                            [{"text": "🎤 Tách Giọng (Vocal)", "callback_data": "extract_vocal"}, {"text": "🥁 Tách Nhạc (Beat)", "callback_data": "extract_beat"}],
                                            [{"text": "📝 Tìm Lời bài hát (.lrc)", "callback_data": "extract_lyric"}],
                                            [{"text": "🌟 Xử lý TẤT CẢ (Vocal, Beat, Lời)", "callback_data": "extract_all"}],
                                            [{"text": "❌ Hủy bỏ file này", "callback_data": "cancel_audio_name"}]
                                        ]
                                    }
                                    await send_telegram_message(f"✅ Đã chốt tên: <b>{text}</b>\n\nSếp muốn trích xuất những file nào?", reply_markup=kb_options)
                                    continue

                                # Lệnh Terminal Xuyên không
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
                                    await send_telegram_message("⏳ <i>AI đang suy nghĩ...</i>")
                                    try:
                                        # 🚀 GỌI NÃO BỘ MỚI TẠI ĐÂY
                                        from core.bot_ai import process_telegram_ai
                                        ai_res = await process_telegram_ai(chat_id, text)
                                        
                                        reply = f"🤖 <b>AI:</b>\n\n{ai_res['reply']}"
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
                                
                                # XÁC NHẬN DÙNG TÊN MẶC ĐỊNH (BƯỚC 1 -> BƯỚC 2)
                                if data_cb == "confirm_audio_name":
                                    if chat_id in pending_audio_tasks and pending_audio_tasks[chat_id].get("step") == "name":
                                        suggested = pending_audio_tasks[chat_id]["suggested_name"]
                                        pending_audio_tasks[chat_id]["chosen_name"] = suggested
                                        pending_audio_tasks[chat_id]["step"] = "option"
                                        
                                        kb_options = {
                                            "inline_keyboard": [
                                                [{"text": "🎤 Tách Giọng (Vocal)", "callback_data": "extract_vocal"}, {"text": "🥁 Tách Nhạc (Beat)", "callback_data": "extract_beat"}],
                                                [{"text": "📝 Tìm Lời bài hát (.lrc)", "callback_data": "extract_lyric"}],
                                                [{"text": "🌟 Xử lý TẤT CẢ (Vocal, Beat, Lời)", "callback_data": "extract_all"}],
                                                [{"text": "❌ Hủy bỏ file này", "callback_data": "cancel_audio_name"}]
                                            ]
                                        }
                                        await send_telegram_message(f"✅ Đã chốt tên: <b>{suggested}</b>\n\nSếp muốn trích xuất những file nào?", reply_markup=kb_options)
                                    else:
                                        await send_telegram_message("⚠️ Yêu cầu đã hết hạn hoặc bị lỗi trạng thái.")
                                        
                                # NHẬN LỰA CHỌN TRÍCH XUẤT (BƯỚC 2 -> CHẠY NGẦM)
                                elif data_cb in ["extract_vocal", "extract_beat", "extract_lyric", "extract_all"]:
                                    if chat_id in pending_audio_tasks and pending_audio_tasks[chat_id].get("step") == "option":
                                        task_data = pending_audio_tasks.pop(chat_id)
                                        option_map = {
                                            "extract_vocal": "vocal",
                                            "extract_beat": "beat",
                                            "extract_lyric": "lyric",
                                            "extract_all": "all"
                                        }
                                        selected_option = option_map[data_cb]
                                        asyncio.create_task(trigger_audio_processing(chat_id, task_data["file_id"], task_data["chosen_name"], task_data["original_filename"], selected_option))
                                    else:
                                        await send_telegram_message("⚠️ Yêu cầu không còn hiệu lực.")
                                        
                                # HỦY BỎ FILE
                                elif data_cb == "cancel_audio_name":
                                    if chat_id in pending_audio_tasks:
                                        pending_audio_tasks.pop(chat_id)
                                        await send_telegram_message("❌ Đã hủy quá trình xử lý dự án.")

                                # CÁC LỆNH HỆ THỐNG KHÁC (Tunnel, HW, Cleanup...)
                                from api.dashboard import api_status_db
                                from scripts.network_tunnel import start_tunnel, stop_tunnel, get_tunnel_url
                                
                                if data_cb == "toggle_tunnel":
                                    current = api_status_db["internet_tunnel"]["active"]
                                    api_status_db["internet_tunnel"]["active"] = not current
                                    if not current:
                                        start_tunnel()
                                        await send_telegram_message("⏳ Đang bật Cloudflare Tunnel (Cổng 16868)...")
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
                                    cpu = psutil.cpu_percent(interval=0.5)
                                    ram = psutil.virtual_memory()
                                    disk = psutil.disk_usage('/')
                                    msg = (f"📊 <b>BÁO CÁO PHẦN CỨNG:</b>\n\n"
                                           f"🎛️ CPU: {cpu}%\n"
                                           f"🧠 RAM: {ram.percent}% ({round(ram.used/(1024**3), 1)}GB / {round(ram.total/(1024**3), 1)}GB)\n"
                                           f"💾 Bộ nhớ: {disk.percent}% (Trống {round(disk.free/(1024**3), 1)}GB)\n"
                                           f"🔋 Tình trạng Pin: {get_device_battery()}")
                                    await send_telegram_message(msg)
                                    
                                elif data_cb == "top_processes":
                                    procs = sorted([p.info for p in psutil.process_iter(['pid', 'name', 'memory_percent']) if p.info['memory_percent']], key=lambda p: p['memory_percent'], reverse=True)[:5]
                                    proc_str = "\n".join([f"▪️ <b>{p['name']}</b>: {p['memory_percent']:.1f}% RAM" for p in procs])
                                    await send_telegram_message(f"🔬 <b>TOP 5 ỨNG DỤNG NGỐN RAM:</b>\n\n{proc_str}")
                                    
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
                                        os.remove(zip_file_path)
                                        await send_telegram_message("✅ Gửi mã nguồn thành công!")
                                    except Exception as e:
                                        await send_telegram_message(f"❌ Lỗi sao lưu: {e}")
                                    
                                elif data_cb == "restart_api":
                                    await send_telegram_message("🔄 Đã làm mới hệ thống thành công trên cổng 16868!")
                                
                                await client.post(f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/answerCallbackQuery", json={"callback_query_id": cb_id})
                                
            except Exception as e:
                await asyncio.sleep(5)
            await asyncio.sleep(1)