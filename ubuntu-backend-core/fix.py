import os

FILE_IN = "GameMidlet.class"
FILE_OUT = "GameMidlet_Patched.class"

def patch_class():
    print("=======================================================")
    print(" 🛠️ TOOL CHỐT HẠ: FIX TRIỆT ĐỂ LỖI LAN (VERSION 6) 🛠️")
    print("=======================================================\n")

    if not os.path.exists(FILE_IN):
        print(f"[x] LỖI: Không tìm thấy file '{FILE_IN}'!")
        return

    with open(FILE_IN, "rb") as f:
        data = bytearray(f.read())

    ip = input("👉 Nhập địa chỉ IP Wi-Fi CỦA MÁY CHỦ (VD: 192.168.1.15): ").strip()
    if not ip:
        print("[x] Bạn chưa nhập IP. Thoát chương trình!")
        return

    # Định dạng lại Link HTTP chuẩn cho mảng D
    http_ip = f"http://{ip}"

    # TỪ ĐIỂN THAY THẾ (Ép toàn bộ về IP của bạn, không chừa 1 đường lùi)
    replacements = {
        # Fix mảng B (Dải IP trần)
        "127.0.0.1": ip,
        "192.168.110.123": ip,
        "112.78.1.25": ip,
        
        # Fix mảng D (Dải Link HTTP) -> Ép máy khác tìm đến máy chủ của bạn
        "http://127.0.0.1": http_ip,
        "http://127.0.0.1/": http_ip + "/",
        "http://teamobi.com/srvips/avatar2.txt": http_ip,
        "http://trochoididong.us/srvips/avatar_C.txt": http_ip,
        "http://teamobi.com/srvips/avatarinterd2.txt": http_ip,
        "http://trochoididong.us/srvips/avatarinter_C.txt": http_ip,
        
        # Việt hóa
        "Xu So Dieu Ky": "Xứ Sở Diệu Kỳ",
        "Thanh Pho Hoan My": "Thành Phố Hoàn Mỹ",
        "Thanh Pho Tam Giao": "Thành Phố Tam Giao",
        "Thanh Pho Than Thoai": "Thành Phố Thần Thoại",
        "Thanh Pho Tri Ky": "Thành Phố Tri Kỷ",
        "Thanh Pho Hoa Binh": "Thành Phố Hòa Bình",
        "Thanh Pho Dieu Ky": "Thành Phố Diệu Kỳ",
        "Thanh Pho Mong Mo": "Thành Phố Mộng Mơ",
        "Xu So Than Tien": "Xứ Sở Thần Tiên",
        "Thanh Pho Bao Binh": "Thành Phố Bảo Bình",
        "Thanh Pho Nhan Ma": "Thành Phố Nhân Mã",
        "Thanh Pho Su Tu": "Thành Phố Sư Tử",
        "International Server": "Máy Chủ Quốc Tế",
        "Aries City": "Thành Phố Bạch Dương"
    }

    pos = 0

    def read_u2():
        nonlocal pos
        val = int.from_bytes(data[pos:pos+2], 'big')
        pos += 2
        return val

    def read_u4():
        nonlocal pos
        val = int.from_bytes(data[pos:pos+4], 'big')
        pos += 4
        return val

    magic = read_u4()
    if magic != 0xCAFEBABE:
        print("[x] File không hợp lệ!")
        return

    minor = read_u2()
    major = read_u2()
    cp_count = read_u2()

    patched_count = 0
    i = 1
    
    print(f"\n[+] Đang xử lý bóc tách {cp_count} biến...")
    
    while i < cp_count:
        tag = data[pos]
        pos += 1
        
        if tag == 1:
            length = read_u2()
            try:
                string_val = data[pos:pos+length].decode('utf-8')
            except:
                string_val = ""
            
            if string_val in replacements:
                new_str = replacements[string_val]
                new_bytes = new_str.encode('utf-8')
                new_len = len(new_bytes)
                
                # Ghi đè vào file
                data[pos-2:pos] = new_len.to_bytes(2, 'big')
                data[pos:pos+length] = new_bytes
                
                print(f"  [v] Đã cập nhật: '{string_val}' -> '{new_str}'")
                
                pos = pos + new_len
                patched_count += 1
            else:
                pos += length
                
        elif tag in (3, 4, 9, 10, 11, 12): pos += 4
        elif tag in (5, 6): 
            pos += 8
            i += 1 
        elif tag in (7, 8, 16): pos += 2
        elif tag == 15: pos += 3
        elif tag == 18: pos += 4
        
        i += 1

    # Fix Port
    data_bytes = bytes(data)
    for old_p in [14444, 18128]:
        old_b = b'\x11' + old_p.to_bytes(2, 'big')
        new_b = b'\x11' + (19128).to_bytes(2, 'big')
        c = data_bytes.count(old_b)
        if c > 0:
            data_bytes = data_bytes.replace(old_b, new_b)
            print(f"  [v] Đã định tuyến {c} Port {old_p} -> 19128")

    with open(FILE_OUT, "wb") as f:
        f.write(data_bytes)
        
    print(f"\n[+] XONG! File xuất ra tại: {FILE_OUT}")
    print("[+] Mảng D đã được trỏ về IP LAN của bạn. Mọi điện thoại sẽ vào được game!")

if __name__ == '__main__':
    patch_class()