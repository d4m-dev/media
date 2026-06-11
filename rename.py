import os
import re

# --- CẤU HÌNH ---
# 👉 THAY ĐỔI ĐƯỜNG DẪN NÀY tới thư mục chứa ảnh bạn muốn đổi tên.
# Ví dụ: 'HinhNenDep.com/images/aodai/dthuha.05'
TARGET_FOLDER = 'HinhNenDep.com/src/images/ngaunhien'

# --- CÁC ĐỊNH DẠNG ẢNH HỢP LỆ ---
VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')

def rename_images_in_folder(folder_path):
    """
    Đổi tên tất cả các file ảnh trong một thư mục theo định dạng số thứ tự.
    Ví dụ: 1_img.jpg, 2_img.jpg, ...
    """
    print(f"🔍 Bắt đầu quét thư mục: '{folder_path}'")

    if not os.path.isdir(folder_path):
        print(f"❌ Lỗi: Thư mục '{folder_path}' không tồn tại.")
        return

    # 1. Lấy danh sách tất cả các file, tách riêng file ảnh và các file khác
    try:
        all_files = os.listdir(folder_path)
        image_files = []
        other_files_count = 0
        for f in all_files:
            if os.path.isfile(os.path.join(folder_path, f)):
                if f.lower().endswith(VALID_EXTENSIONS):
                    image_files.append(f)
                else:
                    other_files_count += 1
    except Exception as e:
        print(f"❌ Lỗi khi đọc thư mục: {e}")
        return

    if other_files_count > 0:
        print(f"ℹ️  Đã tìm thấy và sẽ bỏ qua {other_files_count} file không phải là ảnh.")

    if not image_files:
        print("✅ Không tìm thấy file ảnh nào để đổi tên.")
        return

    # 2. Sắp xếp các file theo thứ tự tên hiện tại (alphabetical) để đảm bảo thứ tự nhất quán
    # Sử dụng Natural Sort để sắp xếp số đúng thứ tự (1, 2, 10 thay vì 1, 10, 2)
    image_files.sort(key=lambda f: [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', f)])
    print(f"✅ Tìm thấy {len(image_files)} file ảnh. Bắt đầu đổi tên...")

    # 3. Bắt đầu vòng lặp đổi tên
    count = 1
    renamed_count = 0
    skipped_count = 0
    
    for old_filename in image_files:
        try:
            # Lấy phần mở rộng của file (ví dụ: .jpg)
            _, extension = os.path.splitext(old_filename)
            new_filename = f"{count}_img{extension.lower()}"

            old_filepath = os.path.join(folder_path, old_filename)
            new_filepath = os.path.join(folder_path, new_filename)

            # Nếu tên cũ và tên mới giống hệt nhau, bỏ qua để tránh lỗi không cần thiết
            if old_filename == new_filename:
                print(f"   -> Bỏ qua (tên đã đúng): '{old_filename}'")
                skipped_count += 1
                count += 1
                continue

            # Thực hiện đổi tên
            os.rename(old_filepath, new_filepath)
            print(f"   -> Đã đổi: '{old_filename}'  =>  '{new_filename}'")
            
            count += 1
            renamed_count += 1
        except FileExistsError:
            print(f"❌ Lỗi: Không thể đổi tên '{old_filename}' thành '{new_filename}' vì file đích đã tồn tại. Vui lòng dọn dẹp thư mục và thử lại.")
            break # Dừng lại nếu có xung đột không mong muốn
        except Exception as e:
            print(f"❌ Lỗi khi đổi tên file '{old_filename}': {e}")

    print("\n🎉 Hoàn tất!")
    if renamed_count > 0: print(f"   - Đã đổi tên: {renamed_count} file.")
    if skipped_count > 0: print(f"   - Đã bỏ qua: {skipped_count} file (tên đã đúng).")

if __name__ == "__main__":
    if 'path/to/your/image/folder' in TARGET_FOLDER:
        print("\n‼️  VUI LÒNG MỞ FILE `rename.py` VÀ CHỈNH SỬA BIẾN `TARGET_FOLDER` TRƯỚC KHI CHẠY.\n")
    else:
        rename_images_in_folder(TARGET_FOLDER)