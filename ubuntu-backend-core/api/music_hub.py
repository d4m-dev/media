import os
import re
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse, FileResponse

# Khởi tạo luồng Router độc lập cho tính năng Music Hub
router = APIRouter(
    prefix="/api/music",
    tags=["Music Hub API"]
)

# Nhận diện đường dẫn gốc: ubuntu-backend-core/audio_workspace/music/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC_DIR = os.path.join(BASE_DIR, "audio_workspace", "music")

def chunked_file_reader(file_path: str, start: int, end: int, chunk_size: int = 1024 * 1024):
    """Cưa file MP3/MP4 thành các khối 1MB để Stream mượt mà"""
    with open(file_path, "rb") as f:
        f.seek(start)
        while (pos := f.tell()) <= end:
            read_size = min(chunk_size, end + 1 - pos)
            yield f.read(read_size)

@router.get("/stream/{folder}/{filename}")
async def stream_media(folder: str, filename: str, request: Request):
    """API Stream trực tiếp file Nhạc (2.mp3, 3.mp3) hoặc Video (4.mp4)"""
    file_path = os.path.join(MUSIC_DIR, folder, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File không tồn tại")
    
    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("Range")
    
    # Định dạng Content-Type dựa trên đuôi file
    content_type = "video/mp4" if filename.endswith(".mp4") else "audio/mpeg"

    if range_header:
        match = re.search(r'bytes=(\d+)-(\d*)', range_header)
        start = int(match.group(1))
        end = int(match.group(2)) if match.group(2) else file_size - 1
        
        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(end - start + 1),
            "Content-Type": content_type,
        }
        return StreamingResponse(chunked_file_reader(file_path, start, end), status_code=206, headers=headers)
    
    headers = {
        "Accept-Ranges": "bytes",
        "Content-Length": str(file_size),
        "Content-Type": content_type,
    }
    return StreamingResponse(chunked_file_reader(file_path, 0, file_size - 1), headers=headers)

@router.get("/cover/{folder}")
async def get_cover(folder: str):
    """API Lấy ảnh bìa (cover.jpg)"""
    cover_path = os.path.join(MUSIC_DIR, folder, "cover.jpg")
    if not os.path.exists(cover_path):
         # Trả về một ảnh mặc định nếu bài hát chưa có cover
         raise HTTPException(status_code=404, detail="Không tìm thấy ảnh bìa")
    return FileResponse(cover_path, media_type="image/jpeg")

@router.get("/lyrics/{folder}")
async def get_lyrics(folder: str):
    """API Đọc file 1.lrc và chuyển thành mảng JSON thời gian thực"""
    lrc_path = os.path.join(MUSIC_DIR, folder, "1.lrc")
    
    if not os.path.exists(lrc_path):
        return {"status": "error", "message": "Bài hát này chưa có file lời (1.lrc)."}

    lyrics_data = []
    try:
        with open(lrc_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                match = re.search(r'\[(\d{2}):(\d{2}\.\d{2,3})\](.*)', line)
                if match:
                    mins = int(match.group(1))
                    secs = float(match.group(2))
                    text = match.group(3).strip()
                    if text:
                        time_ms = int((mins * 60 + secs) * 1000)
                        lyrics_data.append({"time": time_ms, "text": text})
                        
        return {"status": "success", "folder": folder, "lyrics": lyrics_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# 📂 NÂNG CẤP: TỰ ĐỘNG QUÉT THƯ VIỆN NHẠC
# ==========================================
@router.get("/list")
async def get_music_list():
    """
    API Quét thư mục: Tự động tìm tất cả các bài hát sếp đã bỏ vào /music/
    """
    if not os.path.exists(MUSIC_DIR):
        return {"status": "success", "songs": []}

    songs = []
    try:
        # Quét tất cả các thư mục con
        for folder_name in os.listdir(MUSIC_DIR):
            folder_path = os.path.join(MUSIC_DIR, folder_name)
            
            # Chỉ lấy các thư mục (bỏ qua file rác nếu có)
            if os.path.isdir(folder_path):
                # Format lại tên cho đẹp (VD: xuanhuyhoang -> Xuanhuyhoang)
                display_name = folder_name.replace("-", " ").replace("_", " ").title()
                
                songs.append({
                    "id": folder_name,
                    "title": display_name,
                    "cover_api": f"/api/music/cover/{folder_name}"
                })
                
        return {"status": "success", "total": len(songs), "songs": songs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi quét kho nhạc: {str(e)}")