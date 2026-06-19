import sqlite3
import os
import mysql.connector
from mysql.connector import pooling
from core.config import settings

# ==========================================
# --- PHẦN 1: SQLITE CHO ACCESS LOGS ---
# ==========================================
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
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO access_logs (ip_address, method, path, status_code) VALUES (?, ?, ?, ?)",
            (ip, method, path, status_code)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Lỗi ghi log SQLite: {e}")

def get_request_stats():
    try:
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
    except Exception:
        return {"timeline": []}

def get_raw_logs(limit=30):
    """Trích xuất nhật ký dạng chuỗi văn bản thô cho AI đọc hiểu"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT datetime(timestamp, 'localtime'), ip_address, method, path, status_code 
            FROM access_logs ORDER BY id DESC LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return "\n".join([f"[{r[0]}] IP: {r[1]} | {r[2]} {r[3]} | Status: {r[4]}" for r in rows])
    except Exception:
        return "Không thể đọc Access Logs."


# ==========================================
# --- PHẦN 2: MARIADB CHO SOCIAL SERVICES & GAME ---
# ==========================================
class DbManager:
    """Quản lý Connection Pool (Mô phỏng HikariCP của Java)"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DbManager, cls).__new__(cls)
            cls._instance._init_pool()
        return cls._instance

    def _init_pool(self):
        self.pool = None
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name="social_hub_pool",
                pool_size=10,  # Tương đương max_connections
                pool_reset_session=True,
                host=settings.DB_HOST,
                port=int(settings.DB_PORT),
                database=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASS
            )
            print("✅ DB Connection Pool đã được khởi tạo thành công!")
        except Exception as e:
            print(f"⚠️ Khởi tạo MariaDB Pool thất bại (Sẽ thử lại sau): {e}")

    def get_connection(self):
        if self.pool:
            return self.pool.get_connection()
        # Fallback nếu pool bị rớt
        self._init_pool()
        if self.pool:
            return self.pool.get_connection()
        raise Exception("Connection pool chưa được khởi tạo hoặc CSDL đang sập!")


class DbExecutor:
    """Tương đương DbExecutor.java - Chuyên xử lý lệnh SELECT"""
    def __init__(self):
        self.db = DbManager()

    def select_as_list_dict(self, sql, params=None):
        """Đọc data và tự động chuyển thành danh sách Dictionary (Giống selectResultAsListObj)"""
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params or ())
            return cursor.fetchall()
        except Exception as e:
            print(f"⚠️ DbExecutor EXCEPTION: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()  # Trả connection lại cho Pool


class DbInserter:
    """Tương đương DbInserter.java - Chuyên xử lý lệnh INSERT"""
    def __init__(self):
        self.db = DbManager()

    def insert(self, sql, params=None):
        """Thực thi INSERT và trả về ID (Khóa chính) vừa tạo"""
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"⚠️ DbInserter EXCEPTION: {e}")
            if conn: conn.rollback()
            return None
        finally:
            if cursor: cursor.close()
            if conn: conn.close()


class DbUpdater:
    """Tương đương DbUpdater.java - Chuyên xử lý lệnh UPDATE / DELETE"""
    def __init__(self):
        self.db = DbManager()

    def update(self, sql, params=None):
        """Thực thi và trả về số dòng bị ảnh hưởng trong Database"""
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"⚠️ DbUpdater EXCEPTION: {e}")
            if conn: conn.rollback()
            return -1
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

# Khởi tạo sẵn các Instance để các file khác import dùng ngay lập tức
db_manager = DbManager()
db_executor = DbExecutor()
db_inserter = DbInserter()
db_updater = DbUpdater()