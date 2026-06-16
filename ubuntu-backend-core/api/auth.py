from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.security import verify_password, create_access_token, ADMIN_USERNAME
from core.database import db_manager
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 🚀 GỌI BỘ CẤU HÌNH HỆ THỐNG .ENV TỪ CORE
from core.config import settings

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication & SSO"]
)

# Cấu hình máy chủ SMTP mặc định của Google
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_otp_email(to_email: str, otp_code: str, username: str):
    """Hàm nội bộ gửi Email OTP qua Giao thức SMTP bảo mật"""
    
    # 🚀 LẤY TÀI KHOẢN VÀ MẬT KHẨU TỪ FILE .ENV QUA SETTINGS
    sender_email = getattr(settings, "SENDER_EMAIL", None)
    sender_password = getattr(settings, "SENDER_PASSWORD", None)
    
    # Kiểm tra xem sếp đã điền cấu hình trong file .env chưa
    if not sender_email or not sender_password:
        print("⚠️ Lỗi hệ thống: Chưa cấu hình SENDER_EMAIL hoặc SENDER_PASSWORD trong file .env!")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = f"D4M ID System <{sender_email}>"
        msg['To'] = to_email
        msg['Subject'] = "Mã Xác Thực Định Danh - D4M Ecosystem"

        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <div style="max-w: 500px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: center;">
                    <h2 style="color: #3b82f6;">Xác Thực D4M ID</h2>
                    <p>Xin chào <strong>{username}</strong>,</p>
                    <p>Mã OTP để xác thực tài khoản Hệ sinh thái của bạn là:</p>
                    <div style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #8b5cf6; margin: 20px 0; padding: 15px; background: #f3f4f6; border-radius: 8px;">
                        {otp_code}
                    </div>
                    <p style="color: #666; font-size: 14px;">Mã này chỉ có hiệu lực một lần. Vui lòng không chia sẻ mã này cho bất kỳ ai.</p>
                </div>
            </body>
        </html>
        """
        msg.attach(MIMEText(html_body, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Lỗi gửi Email SMTP: {e}")
        return False

# ========================================================
# CÁC CLASS ĐỊNH NGHĨA DỮ LIỆU
# ========================================================
class LoginRequest(BaseModel):
    username: str
    password: str

class SSORegisterRequest(BaseModel):
    username: str
    password: str
    full_name: str
    email: str

class SSOVerifyOTP(BaseModel):
    email: str
    otp: str

# ========================================================
# 1. ĐĂNG NHẬP ADMIN (Giữ nguyên cấu hình cũ)
# ========================================================
@router.post("/login")
async def login(request: LoginRequest):
    if request.username != ADMIN_USERNAME or not verify_password(request.password):
        raise HTTPException(status_code=401, detail="❌ Sai tên đăng nhập hoặc mật khẩu!")
    access_token = create_access_token(data={"sub": request.username, "role": "admin"})
    return {"status": "success", "message": "✅ Đăng nhập thành công!", "access_token": access_token, "token_type": "bearer"}

# ========================================================
# 2. ĐĂNG KÝ NGƯỜI DÙNG SSO D4M ID
# ========================================================
@router.post("/sso/register")
async def register_sso(data: SSORegisterRequest):
    cursor = db_manager.connection.cursor()
    
    # Kiểm tra trùng lặp User hoặc Email
    cursor.execute("SELECT id FROM users WHERE username=%s OR email=%s", (data.username, data.email))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Tài khoản hoặc Email đã tồn tại!")
    
    # Tạo mã OTP ngẫu nhiên 6 số
    otp_code = ''.join(random.choices(string.digits, k=6))
    
    # Tiến hành Gửi Email bảo mật
    mail_sent = send_otp_email(data.email, otp_code, data.username)
    if not mail_sent:
        raise HTTPException(status_code=500, detail="Máy chủ hệ thống gửi mail lỗi, vui lòng kiểm tra lại cấu hình tệp .env")
    
    # Lưu vào CSDL
    sql = """
        INSERT INTO users (username, password_hash, full_name, email, is_verified, otp_code) 
        VALUES (%s, %s, %s, %s, FALSE, %s)
    """
    cursor.execute(sql, (data.username, data.password, data.full_name, data.email, otp_code))
    db_manager.connection.commit()
    
    return {"status": "success", "message": "Đã tạo tài khoản, chờ xác thực OTP."}

# ========================================================
# 3. XÁC THỰC EMAIL (OTP)
# ========================================================
@router.post("/sso/verify")
async def verify_otp(data: SSOVerifyOTP):
    cursor = db_manager.connection.cursor()
    cursor.execute("SELECT id FROM users WHERE email=%s AND otp_code=%s AND is_verified=FALSE", (data.email, data.otp))
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(status_code=400, detail="OTP không hợp lệ hoặc tài khoản đã xác thực!")
        
    # Kích hoạt tài khoản người dùng
    cursor.execute("UPDATE users SET is_verified=TRUE, otp_code=NULL WHERE id=%s", (user[0],))
    db_manager.connection.commit()
    
    return {"status": "success", "message": "Xác thực định danh thành công."}

# ========================================================
# 4. ĐĂNG NHẬP NGƯỜI DÙNG BÌNH THƯỜNG
# ========================================================
@router.post("/sso/login")
async def sso_login(data: LoginRequest):
    cursor = db_manager.connection.cursor()
    cursor.execute("SELECT id, username, is_verified FROM users WHERE (username=%s OR email=%s) AND password_hash=%s", 
                  (data.username, data.username, data.password))
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(status_code=401, detail="Sai thông tin đăng nhập!")
    if not user[2]:  # is_verified == FALSE
        raise HTTPException(status_code=403, detail="Tài khoản chưa được xác thực Email!")
        
    # Tạo Token định danh dùng chung cho toàn hệ sinh thái
    access_token = create_access_token(data={"sub": user[1], "role": "user", "id": user[0]})
    
    return {
        "status": "success", 
        "message": "Đăng nhập thành công!",
        "access_token": access_token
    }