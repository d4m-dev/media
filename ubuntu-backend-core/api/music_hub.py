import os
import re
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse, FileResponse

# Khởi tạo luồng Router độc lập cho tính năng Music Hub
router = APIRouter(
    prefix="/api/music",
    tags=["Music Hub API"]
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC_DIR = os.path.join(BASE_DIR, "audio_workspace", "music")

# ==========================================
# 🔍 HÀM BỔ TRỢ: BÓC TÁCH METADATA TỪ FILE .LRC
# ==========================================
def parse_lrc_metadata(lrc_path: str, default_title: str) -> dict:
    """Đọc file .lrc và trích xuất thông tin ti, ar, al, by nếu có"""
    metadata = {
        "title": default_title,
        "artist": "d4m-dev Studio",
        "album": "Single",
        "by": "AI Engine"
    }
    
    if not os.path.exists(lrc_path):
        return metadata
        
    try:
        with open(lrc_path, "r", encoding="utf-8") as f:
            content = f.read()
            
            # Sử dụng Regex tìm kiếm không phân biệt chữ hoa chữ thường
            ti_match = re.search(r'\[ti:\s*(.*?)\]', content, re.IGNORECASE)
            ar_match = re.search(r'\[ar:\s*(.*?)\]', content, re.IGNORECASE)
            al_match = re.search(r'\[al:\s*(.*?)\]', content, re.IGNORECASE)
            by_match = re.search(r'\[by:\s*(.*?)\]', content, re.IGNORECASE)
            
            if ti_match and ti_match.group(1).strip():
                metadata["title"] = ti_match.group(1).strip()
            if ar_match and ar_match.group(1).strip():
                metadata["artist"] = ar_match.group(1).strip()
            if al_match and al_match.group(1).strip():
                metadata["album"] = al_match.group(1).strip()
            if by_match and by_match.group(1).strip():
                metadata["by"] = by_match.group(1).strip()
    except Exception as e:
        print(f"⚠️ Lỗi bóc dữ liệu LRC: {e}")
        
    return metadata

# ==========================================
# 🎧 LÕI STREAMING & ĐỌC FILE
# ==========================================
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
# 📂 NÂNG CẤP: TỰ ĐỘNG QUÉT & PHÂN LOẠI THƯ VIỆN NHẠC
# ==========================================
@router.get("/list")
async def get_music_list():
    """API Quét thư mục & Nhận diện cờ Karaoke/Lyrics và Metadata LRC"""
    if not os.path.exists(MUSIC_DIR):
        return {"status": "success", "songs": []}

    songs = []
    try:
        for folder_name in os.listdir(MUSIC_DIR):
            folder_path = os.path.join(MUSIC_DIR, folder_name)
            
            if os.path.isdir(folder_path):
                display_name = folder_name.replace("-", " ").replace("_", " ").title()
                
                # Quét nhanh xem bài này có các vũ khí gì
                files = os.listdir(folder_path)
                has_lyrics = "1.lrc" in files
                has_vocal = "2.mp3" in files
                has_beat = "3.mp3" in files
                has_video = "4.mp4" in files
                
                # Mặc định thông số
                song_title = display_name
                artist_name = "d4m-dev Studio"
                album_name = "Single"

                # Đọc metadata từ 1.lrc nếu có
                if has_lyrics:
                    meta = parse_lrc_metadata(os.path.join(folder_path, "1.lrc"), display_name)
                    song_title = meta["title"]
                    artist_name = meta["artist"]
                    album_name = meta["album"]
                
                # Chỉ hiển thị nếu có ít nhất 1 file nhạc/video
                if has_vocal or has_beat or has_video:
                    songs.append({
                        "id": folder_name,
                        "title": song_title,
                        "artist": artist_name,
                        "album": album_name,
                        "cover_api": f"/api/music/cover/{folder_name}",
                        "flags": {
                            "vocal": has_vocal,
                            "beat": has_beat,
                            "lyrics": has_lyrics,
                            "video": has_video
                        }
                    })
                
        return {"status": "success", "total": len(songs), "songs": songs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi quét kho nhạc: {str(e)}")