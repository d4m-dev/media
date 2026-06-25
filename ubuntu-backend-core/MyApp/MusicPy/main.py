import os
import re
from typing import List, Dict, Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
MUSIC_FILES_DIR: str = os.getenv("MUSIC_FILES_DIR", "./music_files")
os.makedirs(MUSIC_FILES_DIR, exist_ok=True)

app = FastAPI(title="MusicPy Backend API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# GIAO DIỆN FRONTEND CHO NGƯỜI DÙNG
# ==========================================
@app.get("/", tags=["Frontend"])
async def serve_frontend():
    html_content = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>d4m-dev Music Player</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #121212; color: #ffffff; padding: 20px; display: flex; justify-content: center; }
            .player-container { width: 100%; max-width: 500px; background: #1e1e1e; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.5); }
            h1 { text-align: center; color: #1db954; margin-top: 0; font-size: 24px; }
            .now-playing { background: #282828; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
            .np-title { font-size: 18px; font-weight: bold; color: #1db954; margin-bottom: 5px; }
            .np-artist { font-size: 14px; color: #b3b3b3; }
            audio { width: 100%; outline: none; margin-bottom: 20px; }
            .song-list { list-style: none; padding: 0; margin: 0; max-height: 400px; overflow-y: auto; }
            .song-item { padding: 12px 15px; border-bottom: 1px solid #333; cursor: pointer; transition: background 0.2s; }
            .song-item:hover { background: #333; }
            .song-title { font-size: 16px; font-weight: bold; color: #fff; margin-bottom: 3px; }
            .song-artist { font-size: 12px; color: #b3b3b3; }
            ::-webkit-scrollbar { width: 8px; }
            ::-webkit-scrollbar-thumb { background: #555; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="player-container">
            <h1>🎵 MusicPy Player</h1>
            <div class="now-playing" id="nowPlaying">
                <div class="np-title" id="npTitle">Chưa chọn bài hát</div>
                <div class="np-artist" id="npArtist">...</div>
            </div>
            <audio id="audioPlayer" controls></audio>
            <ul class="song-list" id="songList">
                <li class="song-item">Đang tải danh sách bài hát...</li>
            </ul>
        </div>

        <script>
            let currentSongs = [];

            fetch('/music/')
                .then(response => response.json())
                .then(songs => {
                    currentSongs = songs;
                    const list = document.getElementById('songList');
                    list.innerHTML = ''; 
                    
                    if (songs.length === 0) {
                        list.innerHTML = '<li class="song-item">Không tìm thấy bài hát nào.</li>';
                        return;
                    }

                    songs.forEach((song, index) => {
                        let li = document.createElement('li');
                        li.className = 'song-item';
                        li.innerHTML = `
                            <div class="song-title">${song.title}</div>
                            <div class="song-artist">${song.artist}</div>
                        `;
                        li.onclick = () => playSong(index);
                        list.appendChild(li);
                    });
                })
                .catch(err => {
                    document.getElementById('songList').innerHTML = '<li class="song-item" style="color:red;">Lỗi tải dữ liệu!</li>';
                });

            function playSong(index) {
                const song = currentSongs[index];
                const player = document.getElementById('audioPlayer');
                
                document.getElementById('npTitle').innerText = song.title;
                document.getElementById('npArtist').innerText = song.artist;
                
                const encodedPath = song.path.split('/').map(encodeURIComponent).join('/');
                player.src = '/music/' + encodedPath;
                player.play();
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# ==========================================
# CÁC HÀM TIỆN ÍCH (UTILS)
# ==========================================
def format_folder_name(filename: str) -> str:
    """
    Tạo tên thư mục chuẩn từ tên file theo chuẩn PascalCase.
    VD: 'bat con buom vang.mp3'   -> 'BatConBuomVang'
    VD: 'bat_con_buom_vang.jpg'   -> 'BatConBuomVang'
    VD: 'bat-con-buom-vang.lrc'   -> 'BatConBuomVang'
    """
    # 1. Cắt bỏ đuôi file (chỉ lấy phần tên)
    base_name = os.path.splitext(filename)[0]
    
    # 2. Thay thế tất cả các ký tự đặc biệt (bao gồm dấu gạch dưới _, gạch ngang -) thành dấu cách
    clean_name = re.sub(r'[^a-zA-Z0-9]', ' ', base_name)
    
    # 3. Viết hoa chữ cái đầu của MỖI TỪ, sau đó xóa sạch khoảng trắng
    # Quá trình: "bat con buom vang" -> "Bat Con Buom Vang" -> "BatConBuomVang"
    pascal_case_name = clean_name.title().replace(" ", "")
    
    # Trả về kết quả, nếu tên file gốc lỡ viết thường dính liền (batconbuomvang) 
    # thì ít nhất nó vẫn ra Batconbuomvang để không bị lỗi.
    return pascal_case_name
    
def parse_lrc_metadata(lrc_path: str) -> dict:
    """Đọc file .lrc và trích xuất title, artist"""
    metadata = {"title": None, "artist": None}
    try:
        with open(lrc_path, 'r', encoding='utf-8') as f:
            content = f.read()
            ti_match = re.search(r'\[ti:\s*(.*?)\]', content, re.IGNORECASE)
            ar_match = re.search(r'\[ar:\s*(.*?)\]', content, re.IGNORECASE)
            if ti_match: metadata['title'] = ti_match.group(1).strip()
            if ar_match: metadata['artist'] = ar_match.group(1).strip()
    except Exception:
        pass
    return metadata

# ==========================================
# API LẤY DỮ LIỆU & XỬ LÝ NHẠC
# ==========================================
@app.post("/upload-music/", tags=["Music"])
async def upload_music(file: UploadFile = File(...)) -> dict:
    """
    Tải lên file (mp3, lrc, jpg, mp4). 
    Hệ thống tự động tạo thư mục dựa trên tên file và lưu vào đó.
    """
    safe_filename = os.path.basename(file.filename)
    
    # 1. Tạo tên thư mục dựa trên tên gốc của file
    folder_name = format_folder_name(safe_filename)
    target_dir = os.path.join(MUSIC_FILES_DIR, folder_name)
    
    # Đảm bảo thư mục (ví dụ: /Batconbuomvang) tồn tại
    os.makedirs(target_dir, exist_ok=True)
    
    # 2. Lưu file vào bên trong thư mục vừa tạo
    file_path = os.path.join(target_dir, safe_filename)

    try:
        contents = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
        return {
            "filename": safe_filename, 
            "folder": folder_name,
            "message": f"File đã được lưu vào thư mục {folder_name}!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lưu file: {e}")

@app.get("/music/", response_model=List[Dict[str, Any]], tags=["Music"])
async def list_music_files() -> List[Dict[str, Any]]:
    """
    Quét nhạc, tìm file .lrc tương ứng và trả về danh sách chi tiết có dấu.
    """
    songs_data = []
    
    for root, dirs, files in os.walk(MUSIC_FILES_DIR):
        for file in files:
            if file.lower().endswith(('.mp3', '.wav', '.flac', '.m4a')):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, MUSIC_FILES_DIR).replace("\\", "/")
                
                # Cấu hình mặc định nếu không có file .lrc
                base_name = os.path.splitext(file)[0]
                song_title = base_name.replace("_", " ").title()
                song_artist = "Unknown Artist"
                
                # Tìm file .lrc cùng tên trong cùng thư mục
                lrc_filename = f"{base_name}.lrc"
                lrc_path = os.path.join(root, lrc_filename)
                
                if os.path.exists(lrc_path):
                    metadata = parse_lrc_metadata(lrc_path)
                    if metadata['title']: song_title = metadata['title']
                    if metadata['artist']: song_artist = metadata['artist']
                
                songs_data.append({
                    "path": rel_path,
                    "title": song_title,
                    "artist": song_artist,
                    "folder": os.path.basename(root)
                })
                
    return songs_data

@app.get("/music/{file_path:path}", tags=["Music"])
async def stream_music(file_path: str, request: Request) -> FileResponse:
    """Stream nội dung file thực tế"""
    abs_base_dir = os.path.abspath(MUSIC_FILES_DIR)
    target_path = os.path.abspath(os.path.join(abs_base_dir, file_path))

    if not target_path.startswith(abs_base_dir):
        raise HTTPException(status_code=403, detail="Cấm truy cập ra ngoài thư mục nhạc.")
    if not os.path.exists(target_path) or not os.path.isfile(target_path):
        raise HTTPException(status_code=404, detail="File không tìm thấy.")

    return FileResponse(target_path, filename=os.path.basename(target_path))