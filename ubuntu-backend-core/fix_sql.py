import os
import re

def clean_teamobi_sql(input_file, output_file):
    print(f"🚀 Bắt đầu chiến dịch dọn dẹp file: {input_file}...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in, \
             open(output_file, 'w', encoding='utf-8') as f_out:
            
            # Bơm khiên bảo vệ Khóa ngoại (Chống lỗi Foreign Key)
            f_out.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
            
            lines_processed = 0
            for line in f_in:
                # 1. Đổi toàn bộ lệnh INSERT INTO thành REPLACE INTO để chống lỗi trùng lặp ID
                if line.strip().startswith("INSERT INTO"):
                    line = line.replace("INSERT INTO", "REPLACE INTO")
                
                # 2. Xóa các dấu escape backslash (\") dư thừa trong mảng JSON animation
                # Chuyển [{\"img\":... thành [{"img":...
                line = line.replace('\\"', '"')
                
                # Ghi dòng đã làm sạch vào file mới
                f_out.write(line)
                lines_processed += 1
            
            # Kích hoạt lại Khóa ngoại sau khi nạp xong
            f_out.write("\nSET FOREIGN_KEY_CHECKS = 1;\n")
            
        print(f"✅ Hoàn tất! Đã thanh tẩy thành công {lines_processed} dòng mã.")
        print(f"✅ File siêu sạch đã ra lò tại: {output_file}")
        print("💡 Sếp có thể dùng file này để nạp thẳng vào MariaDB được rồi!")
        
    except FileNotFoundError:
        print(f"❌ LỖI: Không tìm thấy file '{input_file}'. Sếp kiểm tra lại xem đã copy file SQL gốc vào đây chưa nhé!")
    except Exception as e:
        print(f"❌ LỖI KHÔNG XÁC ĐỊNH: {str(e)}")

if __name__ == "__main__":
    # Tên file SQL gốc của sếp (Chưa qua xử lý)
    RAW_SQL_FILE = 'raw_data.sql'
    
    # Tên file SQL sau khi đã được Script làm sạch
    CLEAN_SQL_FILE = 'clean_data.sql'
    
    # Kích hoạt
    clean_teamobi_sql(RAW_SQL_FILE, CLEAN_SQL_FILE)