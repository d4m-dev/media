-- 1. Khởi tạo Database nếu chưa có và trỏ vào sử dụng
CREATE DATABASE IF NOT EXISTS social_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE social_hub;

-- 2. Bảng theo dõi click ẩn (Cho trang Bio)
CREATE TABLE IF NOT EXISTS bio_tracking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    link_id VARCHAR(50) NOT NULL,
    platform VARCHAR(50) NOT NULL,
    ip_address VARCHAR(100),
    user_agent TEXT,
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Bảng lưu trữ lịch sử tra cứu Thần số học (Tính năng mở rộng)
CREATE TABLE IF NOT EXISTS numerology_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    birth_date VARCHAR(20) NOT NULL,
    life_path_number INT,
    ip_address VARCHAR(100),
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);