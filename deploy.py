import os
import subprocess
import datetime
import sys
import time
import threading
import itertools
import shutil
import socket

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

def run_command(command):
    """Chạy lệnh shell và trả về (stdout, stderr)"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, encoding='utf-8')
        return result.stdout, None
    except subprocess.CalledProcessError as e:
        return None, e.stderr

def check_internet():
    """Kiểm tra kết nối internet."""
    try:
        # Thử kết nối đến Google DNS (8.8.8.8) port 53
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def generate_smart_commit_message():
    """Tạo commit message thông minh dựa trên file thay đổi."""
    status_out, _ = run_command("git status --porcelain")
    if not status_out:
        return None
    
    lines = status_out.strip().splitlines()
    # Lấy tên file từ output (bỏ qua 3 ký tự đầu: "M  ", "?? ", v.v.)
    files = [line[3:] for line in lines if len(line) > 3]
    
    if not files: return None
    
    if len(files) == 1:
        return f"Update {files[0]}"
    elif len(files) <= 3:
        return f"Update {', '.join(files)}"
    else:
        # Thử tìm thư mục chung
        try:
            common = os.path.commonpath(files)
            if common:
                return f"Update {len(files)} files in {common}/"
        except ValueError:
            pass
        return f"Update {len(files)} files: {', '.join(files[:2])}..."

def is_git_corrupted(stderr):
    """Kiểm tra xem thông báo lỗi có phải do kho Git bị hỏng không."""
    if not stderr:
        return False
    corruption_keywords = ["empty", "fatal: unable to read", "corrupt", "malformed"]
    return any(keyword in stderr.lower() for keyword in corruption_keywords)

def repair_git():
    """Quy trình sửa lỗi Git mạnh mẽ, có thanh tiến trình."""
    print(f"\n{Colors.HEADER}--- BẮT ĐẦU QUY TRÌNH SỬA LỖI GIT ---{Colors.ENDC}")

    with Spinner("Đang lấy URL remote..."):
        remote_url, _ = run_command("git remote get-url origin")

    if not remote_url or not remote_url.strip():
        print(f"\n{Colors.FAIL}❌ Không tìm thấy Remote URL. Không thể tự động khôi phục.{Colors.ENDC}")
        return False

    with Spinner("Đang xóa cấu trúc Git cũ..."):
        if os.path.exists(".git"):
            try:
                shutil.rmtree('.git')
            except OSError as e:
                print(f"\n{Colors.FAIL}❌ Không thể xóa thư mục .git: {e}. Vui lòng thử xóa thủ công.{Colors.ENDC}")
                return False

    with Spinner("Đang khởi tạo lại Git..."):
        run_command("git init")
        run_command(f"git remote add origin {remote_url.strip()}")
        run_command("git branch -M main")

    print(f"\n{Colors.OKGREEN}✅ Đã làm sạch và khôi phục môi trường Git.{Colors.ENDC}")
    print(f"{Colors.HEADER}--- KẾT THÚC SỬA LỖI ---{Colors.ENDC}")
    return True

def fix_git_lock():
    """Xóa file index.lock nếu tồn tại để giải quyết xung đột process."""
    lock_file = os.path.join(".git", "index.lock")
    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
            print(f"\n{Colors.WARNING}⚠️  Đã tự động xóa file khóa bị kẹt (.git/index.lock).{Colors.ENDC}")
            return True
        except OSError:
            return False
    return False

def sync_with_remote():
    """Tự động đồng bộ với remote: stash -> pull --rebase -> stash pop."""
    print(f"\n{Colors.OKBLUE}- Đang tự động đồng bộ với remote...{Colors.ENDC}")

    with Spinner("Cất giữ thay đổi (stash)..."):
        stash_stdout, stash_err = run_command("git stash push --keep-index --include-untracked")
    if stash_err:
        print(f"\n{Colors.FAIL}❌ Không thể stash: {stash_err}{Colors.ENDC}")
        return False

    with Spinner("Kéo thay đổi từ server (pull --rebase)..."):
        _, pull_err = run_command("git pull --rebase")

    if pull_err:
        print(f"\n{Colors.FAIL}❌ Lỗi khi pull/rebase (có thể do xung đột - conflict): {pull_err}{Colors.ENDC}")
        print("   - Đang cố gắng hủy rebase và khôi phục stash...")
        run_command("git rebase --abort")
        run_command("git stash pop")
        print("   - Vui lòng giải quyết xung đột thủ công và chạy lại deploy.")
        return False

    if "No local changes to save" not in stash_stdout:
        with Spinner("Áp dụng lại thay đổi (stash pop)..."):
            _, pop_err = run_command("git stash pop")
        if pop_err:
            print(f"\n{Colors.FAIL}❌ Lỗi khi pop stash (có thể do xung đột): {pop_err}{Colors.ENDC}")
            print("   - Vui lòng giải quyết xung đột thủ công và chạy lại deploy.")
            return False

    print(f"{Colors.OKGREEN}✅ Đồng bộ thành công.{Colors.ENDC}")
    return True

def attempt_push():
    """Thử đẩy code lên server, có cơ chế thử lại."""
    current_branch_raw, err = run_command("git rev-parse --abbrev-ref HEAD")
    if err: return False, err
    current_branch = current_branch_raw.strip()

    push_command = f"git push origin {current_branch} --force-with-lease"
    for attempt in range(3):  # PUSH_RETRIES = 3
        print(f"\n{Colors.OKBLUE}- Đang đẩy lên nhánh '{current_branch}' (lần {attempt + 1}/3)...{Colors.ENDC}")
        with Spinner("Đang đẩy code..."):
            _, stderr = run_command(push_command)
        if not stderr:
            return True, None  # Thành công

        print(f"{Colors.WARNING}⚠️  Lỗi: {stderr.strip().splitlines()[-1]}{Colors.ENDC}")

        if "non-fast-forward" in stderr or "updates were rejected" in stderr:
            print("   -> Remote có thay đổi mới.")
            if sync_with_remote():
                print("   -> Đồng bộ xong, thử đẩy lại ngay lập tức...")
                continue  # Thử lại ngay mà không cần chờ
            else:
                return False, "Auto-sync failed"

        if is_git_corrupted(stderr):
            return False, stderr  # Báo cho vòng lặp chính biết cần sửa lỗi

        if attempt < 2:  # PUSH_RETRIES - 1
            print(f"   -> Thử lại sau 5 giây...")
            time.sleep(5)
    print(f"{Colors.FAIL}❌ Đã thử đẩy lên nhiều lần nhưng không thành công.{Colors.ENDC}")
    return False, stderr

def optimize_repo():
    """Tối ưu hóa repository."""
    with Spinner("Đang tối ưu hóa repository (git gc)..."):
        run_command("git gc --auto")

def deploy_process(custom_message=None, yes_to_all=False):
    """Chạy toàn bộ quy trình deploy một lần. Trả về: 'success', 'failed', 'needs_repair'"""

    skip_commit = False # Cờ để bỏ qua bước commit nếu chỉ cần push

    # Bước 1: Kiểm tra trạng thái
    with Spinner("Đang kiểm tra trạng thái..."):
        if not os.path.exists(".git"):
            print(f"\n{Colors.FAIL}❌ Thư mục hiện tại chưa được khởi tạo Git!{Colors.ENDC}")
            return "failed"
        status, err = run_command("git status --porcelain")

    if err:
        if is_git_corrupted(err): return "needs_repair"
        print(f"\n{Colors.FAIL}❌ Lỗi kiểm tra trạng thái Git: {err}{Colors.ENDC}")
        return "failed"

    if not status.strip():
        # Kiểm tra xem có commit nào chưa được push không
        current_branch_raw, _ = run_command("git rev-parse --abbrev-ref HEAD")
        current_branch = current_branch_raw.strip() if current_branch_raw else "main"
        unpushed_raw, _ = run_command(f"git log origin/{current_branch}..HEAD --oneline")

        if unpushed_raw and unpushed_raw.strip():
            print(f"\n{Colors.WARNING}⚠️  Phát hiện commit đã tạo nhưng chưa đẩy lên server. Đang tiến hành đẩy...{Colors.ENDC}")
            skip_commit = True
        else:
            print(f"\n{Colors.WARNING}✅ Không có thay đổi nào mới. Mọi thứ đã được {Colors.OKGREEN}đồng bộ{Colors.ENDC}.{Colors.ENDC}")
            return "success"

    # Bước 4: Tạo commit
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not skip_commit:
        # Bước 2: Thêm file
        with Spinner("Đang thêm file (git add)..."):
            _, err = run_command("git add .")
        
        if err and "index.lock" in err:
            if fix_git_lock():
                with Spinner("Đang thử lại thêm file (git add)..."):
                    _, err = run_command("git add .")

        if err:
            if is_git_corrupted(err): return "needs_repair"
            print(f"\n{Colors.FAIL}❌ Lỗi khi 'git add': {err}{Colors.ENDC}")
            return "failed"

        # Bước 3: Kiểm tra file lớn
        MAX_FILE_SIZE_MB = 80  # Cảnh báo file lớn hơn 80MB
        with Spinner("Đang kiểm tra kích thước file..."):
            large_files = []
            staged_files_raw, _ = run_command("git diff --name-only --staged")
            if staged_files_raw:
                for filename in staged_files_raw.strip().splitlines():
                    if os.path.isfile(filename):
                        try:
                            size_in_mb = os.path.getsize(filename) / (1024 * 1024)
                            if size_in_mb > MAX_FILE_SIZE_MB:
                                large_files.append((filename, size_in_mb))
                        except OSError:
                            pass # Bỏ qua nếu file không tồn tại (ví dụ: đã bị xóa sau khi add)

        if large_files:
            print(f"\n\n{Colors.WARNING}⚠️  CẢNH BÁO: Phát hiện các file có dung lượng lớn hơn giới hạn!{Colors.ENDC}")
            for filename, size in large_files:
                print(f"   - {filename} ({size:.2f} MB)")

            if not yes_to_all:
                answer = input("👉 Bạn có muốn tiếp tục commit không? (y/n): ").lower().strip()
                if answer != 'y':
                    print(f"{Colors.FAIL}❌ Đã hủy bởi người dùng. Hãy dùng 'git reset' để loại bỏ các file lớn.{Colors.ENDC}")
                    return "failed"

        if custom_message:
            commit_message = custom_message
        else:
            # Chế độ tự động: Tạo message thông minh
            smart_msg = generate_smart_commit_message()
            if smart_msg:
                commit_message = f"{smart_msg} ({current_time})"
            else:
                commit_message = f"Auto-commit changes at {current_time}"

        safe_commit_message = commit_message.replace('"', '\\"')
        print(f"\n{Colors.OKCYAN}📝 Đang tạo commit với message: \"{commit_message}\"{Colors.ENDC}")
        with Spinner("Đang tạo commit..."):
            _, err = run_command(f'git commit -m "{safe_commit_message}"')

        if err and "index.lock" in err:
            if fix_git_lock():
                with Spinner("Đang thử lại tạo commit..."):
                    _, err = run_command(f'git commit -m "{safe_commit_message}"')

        # Lỗi "nothing to commit" không phải là lỗi nghiêm trọng, có thể bỏ qua
        if err and "nothing to commit" not in err and "no changes added to commit" not in err:
            if is_git_corrupted(err): return "needs_repair"
            print(f"\n{Colors.FAIL}❌ Lỗi khi 'git commit': {err}{Colors.ENDC}")
            return "failed"

    # Bước 5: Xác nhận và Đẩy lên server
    current_branch_raw, _ = run_command("git rev-parse --abbrev-ref HEAD")
    current_branch = current_branch_raw.strip() if current_branch_raw else "main"

    if not yes_to_all:
        print("\n") # Thêm dòng trống cho dễ nhìn
        answer = input(f"🤔  Sẵn sàng đẩy các thay đổi lên nhánh '{current_branch}'. Xác nhận? (y/n): ").lower().strip()
        if answer != 'y':
            print(f"{Colors.FAIL}❌ Đã hủy bởi người dùng.{Colors.ENDC}")
            return "failed"

    push_success, push_err = attempt_push()
    if not push_success:
        if is_git_corrupted(push_err): return "needs_repair"
        return "failed"

    # Bước 6: Tối ưu hóa (chạy ngầm hoặc nhanh)
    optimize_repo()

    print(f"\n{Colors.OKGREEN}🎉 Triển khai thành công lúc {current_time}!{Colors.ENDC}")
    return "success"

def main():
    """Vòng lặp chính, xử lý việc thử lại và tự động sửa lỗi."""
    print(f"{Colors.HEADER}{Colors.BOLD}=============================================={Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}==    SCRIPT TRIỂN KHAI TỰ ĐỘNG NÂNG CAO    =={Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}=============================================={Colors.ENDC}")

    # Kiểm tra internet
    with Spinner("Đang kiểm tra kết nối mạng..."):
        if not check_internet():
            print(f"\n{Colors.WARNING}⚠️  Cảnh báo: Không có kết nối Internet. Quá trình push có thể thất bại.{Colors.ENDC}")

    yes_to_all = "-y" in sys.argv or "--yes" in sys.argv
    custom_message = None

    if yes_to_all:
        print(f"{Colors.OKCYAN}⚙️  Chế độ tự động (-y) được kích hoạt, sẽ bỏ qua các bước xác nhận.{Colors.ENDC}")

    if "-m" in sys.argv:
        try:
            msg_index = sys.argv.index("-m") + 1
            if msg_index < len(sys.argv):
                custom_message = sys.argv[msg_index]
                # Loại bỏ cờ và message khỏi list để không bị nhầm lẫn
                sys.argv.pop(msg_index)
                sys.argv.pop(msg_index - 1)
                print(f"{Colors.OKBLUE}💬 Sử dụng commit message tùy chỉnh: \"{custom_message}\"{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}⚠️  Cờ -m được cung cấp nhưng thiếu nội dung commit. Sẽ dùng message tự động.{Colors.ENDC}")
        except (ValueError, IndexError):
            pass  # Bỏ qua nếu có lỗi phân tích

    for attempt in range(2):  # MAIN_PROCESS_ATTEMPTS = 2
        if attempt > 0:
            print(f"\n{Colors.WARNING}--- THỬ LẠI TOÀN BỘ QUY TRÌNH (Lần {attempt + 1}/2) ---{Colors.ENDC}")

        result = deploy_process(custom_message, yes_to_all)

        if result == "success":
            return

        if result == "needs_repair":
            if attempt < 1:  # MAIN_PROCESS_ATTEMPTS - 1
                if not repair_git():
                    print(f"\n{Colors.FAIL}❌ Sửa lỗi thất bại. Dừng chương trình.{Colors.ENDC}")
                    break
            else:
                print(f"\n{Colors.FAIL}❌ Đã cố gắng sửa lỗi nhưng vẫn thất bại. Dừng chương trình.{Colors.ENDC}")

        if result == "failed":
            print(f"\n{Colors.FAIL}❌ Gặp lỗi không thể tự sửa. Dừng chương trình.{Colors.ENDC}")
            break

if __name__ == "__main__":
    main()