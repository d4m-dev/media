import os
import re
import sys
import time
import threading
import itertools
from pathlib import Path

# Định nghĩa mã màu ANSI để làm đẹp output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Đảm bảo script luôn chạy từ thư mục chứa nó (để alias hoạt động từ bất kỳ đâu)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Class Spinner để tạo hiệu ứng load xoay tròn
class Spinner:
    def __init__(self, message="Loading...", delay=0.1):
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.delay = delay
        self.message = message
        self.running = False
        self.thread = None

    def spin(self):
        while self.running:
            sys.stdout.write(f"\r{Colors.OKCYAN}{next(self.spinner)}{Colors.ENDC} {self.message}")
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\r' + ' ' * (len(self.message) + 2) + '\r')

    def __enter__(self):
        self.running = True
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write(f"\r{' ' * (len(self.message) + 2)}\r")
        sys.stdout.flush()

def parse_tracks_js(file_path):
    """Phân tích file tracks.js để lấy max_id và danh sách folder đã có."""
    if not os.path.exists(file_path):
        return 0, set()

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Tìm tất cả id
    ids = [int(m) for m in re.findall(r'id:\s*(\d+)', content)]
    max_id = max(ids) if ids else 0

    # Tìm tất cả folder trong đường dẫn music/
    # Pattern bắt cả relative và absolute url
    folders = set(re.findall(r'music/([^/"]+)/', content))
    
    return max_id, folders

def get_metadata_from_lrc(folder_name):
    """Lấy title và artist từ file lrc."""
    lrc_path = os.path.join('music', folder_name, '1.lrc')
    title = None
    artist = None
    
    if os.path.exists(lrc_path):
        try:
            with open(lrc_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('[ti:'):
                        title = line[4:].split(']')[0].strip()
                    elif line.startswith('[ar:'):
                        artist = line[4:].split(']')[0].strip()
        except Exception:
            pass
    return title, artist

def format_title_from_folder(folder_name):
    return folder_name.replace('-', ' ').replace('_', ' ').title()

def create_track_entry(id, folder, title, artist, mode='relative'):
    if mode == 'relative':
        return f"""  {{
    id: {id},
    title: "{title}",
    artist: "{artist}",
    cover: "../../music/{folder}/cover.jpg",
    audioSrc: "../../music/{folder}/2.mp3",
    instrumentalSrc: "../../music/{folder}/3.mp3",
    videoSrc: "../../music/{folder}/4.mp4",
    lyricSrc: "../../music/{folder}/1.lrc"
  }}"""
    else: # github
        return f"""  {{
    id: {id},
    title: "{title}",
    artist: "{artist}",
    cover: "https://raw.githubusercontent.com/d4m-dev/media/main/music/{folder}/cover.jpg",
    lyricSrc: "https://raw.githubusercontent.com/d4m-dev/media/main/music/{folder}/1.lrc",
    audioSrc: "https://raw.githubusercontent.com/d4m-dev/media/main/music/{folder}/2.mp3",
    instrumentalSrc: "https://raw.githubusercontent.com/d4m-dev/media/main/music/{folder}/3.mp3",
    videoSrc: "https://raw.githubusercontent.com/d4m-dev/media/main/music/{folder}/4.mp4"
  }}"""

def append_to_tracks_file(file_path, new_tracks_data, mode):
    if not os.path.exists(file_path):
        print(f"{Colors.FAIL}❌ Không tìm thấy file {file_path}{Colors.ENDC}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Tìm vị trí kết thúc mảng ];
        last_bracket = content.rfind('];')
        if last_bracket == -1:
            print(f"{Colors.FAIL}❌ Không tìm thấy cấu trúc mảng trong {file_path}{Colors.ENDC}")
            return

        # Xác định ID bắt đầu
        max_id, _ = parse_tracks_js(file_path)
        
        entries = []
        current_id = max_id
        for track in new_tracks_data:
            current_id += 1
            entry = create_track_entry(current_id, track['folder'], track['title'], track['artist'], mode)
            entries.append(entry)

        new_content_str = ",\n\n".join(entries)
        
        # Kiểm tra xem phần trước đó có dấu phẩy chưa
        prefix = content[:last_bracket].rstrip()
        if not prefix.endswith(',') and not prefix.endswith('['):
            prefix += ","
            
        final_content = f"{prefix}\n\n{new_content_str}\n{content[last_bracket:]}"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        print(f"{Colors.OKGREEN}✅ Đã thêm {len(entries)} bài hát vào {os.path.basename(file_path)}{Colors.ENDC}")

    except Exception as e:
        print(f"{Colors.FAIL}❌ Lỗi khi ghi file {file_path}: {e}{Colors.ENDC}")

def get_vite_beta_tracks_path():
    """Lấy đường dẫn đến tracks.js trong thư mục beta của MusicPro.com-vite"""
    vite_beta_path = Path.home() / "projects" / "MusicPro.com-vite-beta"
    return vite_beta_path / "src" / "tracks.js"

def main():
    music_dir = 'music'
    if not os.path.exists(music_dir):
        print(f"{Colors.FAIL}❌ Thư mục music không tồn tại.{Colors.ENDC}")
        return

    # Danh sách các file cần cập nhật
    targets = [
        {'path': 'MusicPro.com-beta/src/tracks.js', 'mode': 'relative'},
        {'path': 'load-track/tracks.js', 'mode': 'github'},
        {'path': 'MusicPro.com/src/tracks.js', 'mode': 'github'},
        {'path': 'MusicPro.com-supabase/src/tracks.js', 'mode': 'github'},
        {'path': 'MusicPro.com-vite/src/tracks.js', 'mode': 'github'},
        {'path': 'MusicPro.com-vite-beta/src/tracks.js', 'mode': 'github'},
        {'path': 'MusicPro.com-python/src/tracks.js', 'mode': 'github'},
    ]

    # Thêm đường dẫn ngoài (nếu có)
    vite_beta_path = get_vite_beta_tracks_path()
    if vite_beta_path.exists():
        targets.append({'path': str(vite_beta_path), 'mode': 'github'})

    print(f"{Colors.HEADER}🔍 Đang quét thư mục nhạc và kiểm tra đồng bộ...{Colors.ENDC}")

    # Lấy danh sách tất cả các thư mục nhạc hợp lệ
    music_folders = []
    for item in sorted(os.listdir(music_dir)):
        item_path = os.path.join(music_dir, item)
        if os.path.isdir(item_path):
            # Kiểm tra xem có phải thư mục nhạc không (có mp3)
            if any(f.endswith('.mp3') for f in os.listdir(item_path)):
                music_folders.append(item)

    if not music_folders:
        print(f"{Colors.WARNING}⚠️  Không tìm thấy thư mục nhạc nào trong 'music/'.{Colors.ENDC}")
        return

    # Duyệt qua từng file đích để kiểm tra và cập nhật
    for target in targets:
        file_path = target['path']
        mode = target['mode']
        
        if not os.path.exists(file_path):
            # Chỉ in cảnh báo nhẹ nếu file không tồn tại (để không làm rối màn hình)
            # print(f"   ⚠️  Bỏ qua {file_path} (Không tìm thấy)")
            continue

        # Lấy danh sách folder đã có trong file này
        _, existing_folders = parse_tracks_js(file_path)
        
        # Tìm các folder chưa có trong file này
        missing_folders = [f for f in music_folders if f not in existing_folders]
        
        if not missing_folders:
            print(f"✅ {file_path}: {Colors.OKGREEN}Đã đồng bộ{Colors.ENDC}")
            continue
            
        print(f"🔄 {file_path}: {Colors.OKCYAN}Phát hiện {len(missing_folders)} bài hát mới. Đang cập nhật...{Colors.ENDC}")
        
        # Chuẩn bị dữ liệu để thêm
        new_tracks_data = []
        for folder in missing_folders:
            lrc_title, lrc_artist = get_metadata_from_lrc(folder)
            title = lrc_title if lrc_title else format_title_from_folder(folder)
            artist = lrc_artist if lrc_artist else "Unknown Artist"
            
            new_tracks_data.append({
                'folder': folder,
                'title': title,
                'artist': artist
            })
            
        # Ghi vào file
        append_to_tracks_file(file_path, new_tracks_data, mode)

    print(f"\n{Colors.OKGREEN}🎉 Hoàn tất kiểm tra và cập nhật tất cả các file!{Colors.ENDC}")

if __name__ == "__main__":
    main()