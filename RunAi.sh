#!/bin/bash

# Đường dẫn thư mục chứa model
MODEL_DIR="$HOME/llama.cpp/models"
PORT=9090
IP_TINH="192.168.110.2"

# Tạo thư mục nếu chưa có
mkdir -p $MODEL_DIR

echo "------------------------------------------"
echo "    HỆ THỐNG QUẢN LÝ AI LOCAL - S26 ULTRA  "
echo "------------------------------------------"
echo " IP MÁY CHỦ: $IP_TINH"
echo "------------------------------------------"
echo "1) Llama-3.1-8B-Q8 (Thông minh nhất - Nặng/Chậm)"
echo "2) Llama-3.1-8B-Q4 (TỐI ƯU - Nhanh hơn, ít tốn RAM)"
echo "3) Llama-3.2-3B (Cân bằng - Tốc độ khá)"
echo "4) Qwen-2.5-1.5B (Siêu nhanh - Nhẹ)"
echo "5) Thoát"
echo "------------------------------------------"
read -p "Chọn Model bạn muốn chạy (1-5): " choice

case $choice in
  1)
    MODEL_NAME="Meta-Llama-3.1-8B-Instruct-Q8_0.gguf"
    ;;
  2)
    MODEL_NAME="Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
    ;;
  3)
    MODEL_NAME="Llama-3.2-3B-Instruct-Q8_0.gguf"
    ;;
  4)
    MODEL_NAME="qwen2.5-1.5b-instruct-q8_0.gguf"
    ;;
  5)
    exit 0
    ;;
  *)
    echo "Lựa chọn không hợp lệ."
    exit 1
    ;;
esac

# Kiểm tra file model có tồn tại không
if [ ! -f "$MODEL_DIR/$MODEL_NAME" ]; then
    echo "Lỗi: Không tìm thấy file $MODEL_NAME tại $MODEL_DIR"
    echo "Bạn cần tải model này về trước khi chạy."
    exit 1
fi

echo "Đang khởi động Model: $MODEL_NAME..."
echo "TRUY CẬP TỪ MÁY KHÁC QUA: http://$IP_TINH:$PORT"

# Tự động mở trình duyệt tại máy hiện tại (vẫn dùng localhost cho máy chủ)
(sleep 3 && termux-open-url http://127.0.0.1:$PORT) &

# Chạy Server AI
# --host 0.0.0.0: QUAN TRỌNG - Cho phép kết nối từ bên ngoài
# -t 8: Tận dụng 8 nhân của Snapdragon
# -c 4096: Bộ nhớ ngữ cảnh 4096 tokens
~/llama.cpp/build/bin/llama-server \
    -m "$MODEL_DIR/$MODEL_NAME" \
    --port $PORT \
    -t 8 \
    -c 4096 \
    --host 0.0.0.0
