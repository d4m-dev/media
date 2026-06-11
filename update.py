import os
import re
import shutil
from pathlib import Path
import subprocess
import datetime
import sys
import time
import threading
import itertools

# Đảm bảo script luôn chạy từ thư mục chứa nó
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

def copy_all_files_excluding_tracks(src_dir, dest_dir):
    """
    Sao chép tất cả các tệp từ thư mục nguồn sang thư mục đích,
    ngoại trừ các tệp có tên là 'tracks.js' và thư mục 'node_modules'.
    """
    src_path = Path(src_dir)
    dest_path = Path(dest_dir)

    # Biến đếm số lượng tệp đã sao chép
    copied_count = 0
    skipped_count = 0

    # Duyệt qua tất cả các tệp trong thư mục nguồn
    for src_file in src_path.rglob('*'):
        if src_file.is_file():
            # Tính toán đường dẫn tương đối từ thư mục nguồn
            rel_path = src_file.relative_to(src_path)

            # Bỏ qua thư mục node_modules
            if 'node_modules' in str(rel_path.parts):
                continue

            # Bỏ qua các tệp có tên là 'tracks.js'
            if src_file.name == 'tracks.js':
                skipped_count += 1
                continue

            dest_file = dest_path / rel_path

            # Tạo thư mục đích nếu chưa tồn tại
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            # Sao chép tệp
            shutil.copy2(src_file, dest_file)
            copied_count += 1

    # Thông báo tổng kết
    if copied_count > 0:
        print(f"✨ Đã cập nhật {copied_count} tệp từ {src_path.name} sang {dest_path.name}")
    else:
        print(f"✅ {dest_path.name}: {Colors.OKGREEN}OK{Colors.ENDC} (không có tệp nào cần cập nhật)")

    if skipped_count > 0:
        print(f"⏭️  Đã bỏ qua {skipped_count} tệp tracks.js và thư mục node_modules")

def run_update_functionality():
    """
    Thực hiện chức năng của update.py: nâng cấp tất cả các tệp từ beta sang production
    """
    # Định nghĩa đường dẫn
    base_path = Path(__file__).parent

    # Xử lý riêng cho MusicPro.com-vite-beta vì nó nằm ở vị trí khác (trong thư mục home)
    vite_beta_home_path = Path.home() / "projects" / "MusicPro.com-vite-beta"
    vite_prod_path = base_path / "MusicPro.com-vite"
    vite_beta_media_path = base_path / "MusicPro.com-vite-beta"

    if vite_beta_home_path.exists():
        # Cập nhật cho thư mục MusicPro.com-vite
        if not vite_prod_path.exists():
            print(f"📁 Tạo thư mục sản xuất {vite_prod_path}")
            vite_prod_path.mkdir(parents=True, exist_ok=True)

        # Sao chép tất cả các tệp từ beta (ở home) sang sản xuất (ở media), ngoại trừ tracks.js
        print(f"🚀 Đang cập nhật MusicPro.com-vite từ home...")
        copy_all_files_excluding_tracks(vite_beta_home_path, vite_prod_path)

        # Cập nhật cho thư mục MusicPro.com-vite-beta trong media (để đồng bộ với home)
        if not vite_beta_media_path.exists():
            print(f"📁 Tạo thư mục beta {vite_beta_media_path}")
            vite_beta_media_path.mkdir(parents=True, exist_ok=True)

        # Sao chép tất cả các tệp từ beta (ở home) sang beta (ở media), ngoại trừ tracks.js
        print(f"🚀 Đang cập nhật MusicPro.com-vite-beta từ home...")
        copy_all_files_excluding_tracks(vite_beta_home_path, vite_beta_media_path)
    else:
        print(f"⚠️  Cảnh báo: Thư mục beta {vite_beta_home_path} không tồn tại!")

    # Các dự án còn lại vẫn ở vị trí cũ
    projects = [
        ("MusicPro.com-beta", "MusicPro.com"),
        ("TroLyAo.com-beta", "TroLyAo.com"),
        ("Instagram.com-beta", "Instagram.com"),
        ("QLChiTieu.com-beta", "QLChiTieu.com"),
        ("HinhNenDep.com-beta", "HinhNenDep.com")
    ]

    # Xử lý các dự án còn lại
    for beta_folder, prod_folder in projects:
        beta_path = base_path / beta_folder
        prod_path = base_path / prod_folder

        # Kiểm tra xem thư mục beta có tồn tại không
        if not beta_path.exists():
            print(f"❌ Lỗi: Thư mục beta {beta_path} không tồn tại!")
            continue

        if not prod_path.exists():
            print(f"📁 Tạo thư mục sản xuất {prod_path}")
            prod_path.mkdir(parents=True, exist_ok=True)

        # Sao chép tất cả các tệp từ beta sang sản xuất, ngoại trừ tracks.js
        print(f"🚀 Đang cập nhật {prod_folder}...")
        copy_all_files_excluding_tracks(beta_path, prod_path)

    print(f"🎉 Nâng cấp hoàn tất!")

def main():
    """Chạy toàn bộ quy trình update."""
    print(f"{Colors.HEADER}{Colors.BOLD}=============================================={Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}==         SCRIPT UPDATE FILE NÂNG CAO        =={Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}=============================================={Colors.ENDC}")

    with Spinner("Đang xử lý toàn bộ quy trình..."):
        print(f"\n{Colors.OKCYAN}🔄 Bắt đầu nâng cấp tệp...{Colors.ENDC}")
        run_update_functionality()
        print(f"{Colors.OKGREEN}✅ Nâng cấp tệp hoàn tất.{Colors.ENDC}")

if __name__ == "__main__":
    main()