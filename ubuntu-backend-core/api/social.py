from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.database import db_manager

router = APIRouter(
    prefix="/api/social",
    tags=["Social Hub DB"]
)

# --- CẤU TRÚC DỮ LIỆU ĐẦU VÀO ---
class UserCreate(BaseModel):
    username: str
    fullname: str
    avatar_url: str = ""

class PostCreate(BaseModel):
    user_id: int
    content: str

# --- ENDPOINTS NGƯỜI DÙNG ---
@router.post("/users")
async def create_user(user: UserCreate):
    """Tạo người dùng mới"""
    conn = db_manager.get_connection()
    if not conn: raise HTTPException(status_code=500, detail="Mất kết nối DB")
    
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO users (username, fullname, avatar_url) VALUES (%s, %s, %s)"
            cursor.execute(sql, (user.username, user.fullname, user.avatar_url))
        conn.commit()
        return {"status": "success", "message": "Đã tạo người dùng", "username": user.username}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="Username đã tồn tại")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users")
async def get_all_users():
    """Lấy danh sách người dùng"""
    conn = db_manager.get_connection()
    if not conn: raise HTTPException(status_code=500, detail="Mất kết nối DB")
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, username, fullname, created_at FROM users ORDER BY id DESC LIMIT 50")
            return {"status": "success", "data": cursor.fetchall()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ENDPOINTS BÀI VIẾT (FEED) ---
@router.post("/posts")
async def create_post(post: PostCreate):
    """Đăng bài viết mới"""
    conn = db_manager.get_connection()
    if not conn: raise HTTPException(status_code=500, detail="Mất kết nối DB")
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO posts (user_id, content) VALUES (%s, %s)"
            cursor.execute(sql, (post.user_id, post.content))
            post_id = cursor.lastrowid
        conn.commit()
        return {"status": "success", "message": "Đăng bài thành công", "post_id": post_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feed")
async def get_news_feed():
    """Lấy bảng tin (Kết hợp thông tin User và Post)"""
    conn = db_manager.get_connection()
    if not conn: raise HTTPException(status_code=500, detail="Mất kết nối DB")
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT p.id as post_id, p.content, p.created_at, 
                       u.id as user_id, u.username, u.fullname, u.avatar_url
                FROM posts p
                JOIN users u ON p.user_id = u.id
                ORDER BY p.created_at DESC LIMIT 20
            """
            cursor.execute(sql)
            return {"status": "success", "data": cursor.fetchall()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))