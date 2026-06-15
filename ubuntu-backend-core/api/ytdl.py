import os
import asyncio
import re
import json
import subprocess
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from urllib.parse import quote, unquote
from api.audio_engine import WORKSPACE_DIR

router = APIRouter(prefix="/api/ytdl", tags=["YouTube Downloader Pro"])

YOUTUBE_DIR = os.path.join(WORKSPACE_DIR, "youtube")
os.makedirs(YOUTUBE_DIR, exist_ok=True)

def sanitize_title(title: str) -> str:
    safe = re.sub(r'[\\/*?:"<>|]', "", title)
    return safe.strip()

class YTDLInfoRequest(BaseModel):
    url: str

class YTDLDownloadRequest(BaseModel):
    url: str
    format: str
    quality: str
    title: str

@router.post("/info")
async def get_video_info(req: YTDLInfoRequest):
    # 🚀 DÙNG ĐÚNG MÔI TRƯỜNG NHƯ TELEGRAM ĐỂ TRÁNH LỖI
    python_exec = os.path.expanduser("~/myenv/bin/python3")
    cmd = f'"{python_exec}" -m yt_dlp --dump-json --no-warnings --no-playlist "{req.url}"'
    
    try:
        result = await asyncio.to_thread(subprocess.run, cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception("Lỗi phân tích: Đảm bảo link đúng và video không bị chặn bản quyền.")
            
        info = json.loads(result.stdout)
        duration = info.get("duration", 0)
        
        # 1. Tính toán dung lượng Audio
        audio_320_size = round((duration * 320) / 8192, 1) if duration else 0
        audio_128_size = round((duration * 128) / 8192, 1) if duration else 0
        
        best_audio_size = 0
        for f in info.get("formats", []):
            if f.get("acodec") != "none" and f.get("vcodec") == "none":
                size = f.get("filesize") or f.get("filesize_approx") or 0
                if size > best_audio_size: best_audio_size = size
        
        # 2. Quét độ phân giải và dung lượng Video
        video_sizes = {}
        for f in info.get("formats", []):
            h = f.get("height")
            if h and h > 0 and f.get("vcodec") != "none":
                size = f.get("filesize") or f.get("filesize_approx") or 0
                if f.get("acodec") == "none": size += best_audio_size
                size_mb = round(size / (1024 * 1024), 1)
                
                if h not in video_sizes or size_mb > video_sizes[h]:
                    video_sizes[h] = size_mb

        # 3. Phân loại cấu trúc trả về
        resolutions = []
        for h in sorted(video_sizes.keys(), reverse=True):
            resolutions.append({"height": h, "size": f"{video_sizes[h]} MB" if video_sizes[h] > 0 else "Chưa rõ"})

        if not resolutions:
            resolutions = [{"height": 1080, "size": "Chưa rõ"}, {"height": 720, "size": "Chưa rõ"}]

        return {
            "status": "success",
            "title": info.get("title", "YouTube Video"),
            "thumbnail": info.get("thumbnail", ""),
            "resolutions": resolutions,
            "audio_sizes": {
                "320": f"{audio_320_size} MB" if audio_320_size else "Chưa rõ",
                "128": f"{audio_128_size} MB" if audio_128_size else "Chưa rõ"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/download")
async def process_download(req: YTDLDownloadRequest):
    safe_title = sanitize_title(req.title) or "Unknown_Video"
    task_dir = os.path.join(YOUTUBE_DIR, safe_title)
    os.makedirs(task_dir, exist_ok=True)
    
    out_tmpl = os.path.join(task_dir, f"d4m-dev_{safe_title}.%(ext)s")
    
    python_exec = os.path.expanduser("~/myenv/bin/python3")
    # 🚀 SIÊU TỐC ĐỘ: Bật tải 5 luồng cùng lúc (--concurrent-fragments 5)
    yt_dlp_base = f'"{python_exec}" -m yt_dlp --concurrent-fragments 5 --no-warnings'

    if req.format == "mp3":
        audio_q = "0" if req.quality == "320" else "5"
        cmd = f'{yt_dlp_base} -f "bestaudio/best" -x --audio-format mp3 --audio-quality {audio_q} -o "{out_tmpl}" "{req.url}"'
    else:
        res = req.quality
        cmd = f'{yt_dlp_base} -f "bestvideo[height<={res}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" --merge-output-format mp4 -o "{out_tmpl}" "{req.url}"'

    try:
        result = await asyncio.to_thread(subprocess.run, cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Lỗi tải (Kiểm tra ffmpeg): {result.stderr}")
        
        downloaded_file = None
        for f in os.listdir(task_dir):
            if f.startswith(f"d4m-dev_{safe_title}") and os.path.isfile(os.path.join(task_dir, f)):
                downloaded_file = f
                break
        
        if not downloaded_file: raise Exception("Không tìm thấy file đầu ra.")
            
        safe_folder_url = quote(safe_title)
        safe_filename_url = quote(downloaded_file)
            
        return {
            "status": "success", 
            "file_name": downloaded_file,
            "download_url": f"/api/ytdl/file/{safe_folder_url}/{safe_filename_url}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/file/{folder}/{filename}")
async def serve_file(folder: str, filename: str):
    real_folder = unquote(folder)
    real_filename = unquote(filename)
    file_path = os.path.join(YOUTUBE_DIR, real_folder, real_filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/octet-stream", filename=real_filename)
    raise HTTPException(status_code=404, detail="File không tồn tại")