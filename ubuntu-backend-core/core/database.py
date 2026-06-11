import sqlite3
import os
import pymysql
from core.config import settings

# --- PHẦN 1: SQLITE CHO ACCESS LOGS ---
DB_PATH = "/storage/emulated/0/coder/media/ubuntu-backend-core/database/logs.db"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            method TEXT,
            path TEXT,
            status_code INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_request(ip, method, path, status_code):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO access_logs (ip_address, method, path, status_code) VALUES (?, ?, ?, ?)",
        (ip, method, path, status_code)
    )
    conn.commit()
    conn.close()

def get_request_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT substr(datetime(timestamp, 'localtime'), 12, 5) as minute, COUNT(*)
        FROM access_logs
        GROUP BY minute
        ORDER BY minute DESC
        LIMIT 10
    ''')
    rows = cursor.fetchall()
    conn.close()
    rows.reverse()
    return {"timeline": [{"time": row[0], "count": row[1]} for row in rows]}

def get_raw_logs(limit=30):
    """Trích xuất nhật ký dạng chuỗi văn bản thô cho AI đọc hiểu"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT datetime(timestamp, 'localtime'), ip_address, method, path, status_code 
        FROM access_logs ORDER BY id DESC LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return "\n".join([f"[{r[0]}] IP: {r[1]} | {r[2]} {r[3]} | Status: {r[4]}" for r in rows])

# --- PHẦN 2: MARIADB CHO SOCIAL SERVICES ---
class MariaDBConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=settings.DB_HOST, port=settings.DB_PORT, user=settings.DB_USER,
                password=settings.DB_PASS, database=settings.DB_NAME, cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            print(f"⚠️ Không thể kết nối MariaDB: {e}")

    def get_connection(self):
        if not self.connection or not self.connection.open:
            self.connect()
        return self.connection

    def init_social_tables(self):
        conn = self.get_connection()
        if not conn: return
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL,
                        fullname VARCHAR(100), avatar_url VARCHAR(255) DEFAULT '',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS posts (
                        id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, content TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS media (
                        id INT AUTO_INCREMENT PRIMARY KEY, post_id INT, file_url VARCHAR(255) NOT NULL,
                        media_type VARCHAR(50) DEFAULT 'image',
                        FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
                    )
                """)
            conn.commit()
        except Exception as e:
            print(f"⚠️ Lỗi khi khởi tạo bảng Social Hub: {e}")

db_manager = MariaDBConnection()