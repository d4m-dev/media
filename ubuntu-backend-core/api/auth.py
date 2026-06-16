from fastapi import APIRouter, HTTPException, Header, UploadFile, File, Depends
from pydantic import BaseModel
from core.security import verify_password, create_access_token, ADMIN_USERNAME
from core.database import db_manager
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import jwt
import shutil
import os
from dotenv import load_dotenv

# Ép hệ thống nạp file .env ngay lập tức
load_dotenv()

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication & SSO"]
)

# Cấu hình máy chủ SMTP mặc định của Google
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_otp_email(to_email: str, otp_code: str, username: str):
    """Hàm nội bộ gửi Email OTP qua Giao thức SMTP bảo mật"""
    
    # LẤY TRỰC TIẾP TỪ FILE .ENV (Không qua class settings nữa)
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    
    # Kênh an toàn: Kiểm tra nếu quên điền .env
    if not sender_email or not sender_password:
        print("⚠️ Lỗi hệ thống: Không tìm thấy SENDER_EMAIL hoặc SENDER_PASSWORD trong file .env!")
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

# Hàm nội bộ: Bóc tách Token để lấy User ID
def get_current_user_id(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Vui lòng đăng nhập lại.")
    token = authorization.split(" ")[1]
    try:
        # Giải mã token (Bypass verify signature cho prototype)
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload.get("id"), payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Token hết hạn hoặc lỗi.")

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

class UpdateProfileRequest(BaseModel):
    full_name: str = None
    dob: str = None
    phone: str = None
    address: str = None

class ChangeEmailRequest(BaseModel):
    new_email: str

class VerifyChangeEmailRequest(BaseModel):
    new_email: str
    otp: str

# ========================================================
# 1. ĐĂNG NHẬP ADMIN
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
    cursor.execute("SELECT id, otp_code FROM users WHERE email=%s AND is_verified=FALSE", (data.email,))
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(status_code=400, detail="Tài khoản không tồn tại hoặc đã xác thực!")
    
    # Tương thích DictCursor và Tuple
    db_otp = user['otp_code'] if isinstance(user, dict) else user[1]
    user_id = user['id'] if isinstance(user, dict) else user[0]

    if db_otp != data.otp:
        raise HTTPException(status_code=400, detail="OTP không hợp lệ!")
    
    # Kích hoạt tài khoản người dùng
    cursor.execute("UPDATE users SET is_verified=TRUE, otp_code=NULL WHERE id=%s", (user_id,))
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
        
    # Tương thích DictCursor và Tuple
    is_verified = user['is_verified'] if isinstance(user, dict) else user[2]
    username = user['username'] if isinstance(user, dict) else user[1]
    user_id = user['id'] if isinstance(user, dict) else user[0]
    
    if not is_verified:  
        raise HTTPException(status_code=403, detail="Tài khoản chưa được xác thực Email!")
        
    # Tạo Token định danh dùng chung
    access_token = create_access_token(data={"sub": username, "role": "user", "id": user_id})
    
    return {
        "status": "success", 
        "message": "Đăng nhập thành công!",
        "access_token": access_token
    }

# ========================================================
# 5. LẤY THÔNG TIN PROFILE HIỆN TẠI
# ========================================================
@router.get("/profile/me")
async def get_my_profile(auth_data: tuple = Depends(get_current_user_id)):
    user_id, username = auth_data
    cursor = db_manager.connection.cursor()
    cursor.execute("SELECT id, username, full_name, email, phone, dob, address, avatar_url FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")
        
    user_dict = user if isinstance(user, dict) else {
        "id": user[0], "username": user[1], "full_name": user[2], 
        "email": user[3], "phone": user[4], "dob": user[5], 
        "address": user[6], "avatar_url": user[7]
    }
    
    # Gắn Avatar mặc định nếu chưa có
    if not user_dict.get("avatar_url"):
        user_dict["avatar_url"] = "/src/favicon/ubuntu-backend/favicon-96x96.png"
        
    return {"status": "success", "data": user_dict}

# ========================================================
# 6. CẬP NHẬT THÔNG TIN CƠ BẢN (Không cần OTP)
# ========================================================
@router.put("/profile/update")
async def update_profile(data: UpdateProfileRequest, auth_data: tuple = Depends(get_current_user_id)):
    user_id, _ = auth_data
    cursor = db_manager.connection.cursor()
    cursor.execute("""
        UPDATE users SET full_name=%s, dob=%s, phone=%s, address=%s WHERE id=%s
    """, (data.full_name, data.dob, data.phone, data.address, user_id))
    db_manager.connection.commit()
    return {"status": "success", "message": "Đã lưu thông tin hồ sơ."}

# ========================================================
# 7. UPLOAD ẢNH ĐẠI DIỆN
# ========================================================
@router.post("/profile/avatar")
async def upload_avatar(file: UploadFile = File(...), auth_data: tuple = Depends(get_current_user_id)):
    user_id, username = auth_data
    
    # Tạo thư mục lưu trữ: public/images/avatar/ten_user/
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    avatar_dir = os.path.join(base_dir, "public", "images", "avatar", username)
    os.makedirs(avatar_dir, exist_ok=True)
    
    # Lưu file
    file_ext = file.filename.split(".")[-1]
    filename = f"avatar_{username}.{file_ext}"
    file_path = os.path.join(avatar_dir, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    avatar_url = f"/images/avatar/{username}/{filename}"
    
    # Cập nhật CSDL
    cursor = db_manager.connection.cursor()
    cursor.execute("UPDATE users SET avatar_url=%s WHERE id=%s", (avatar_url, user_id))
    db_manager.connection.commit()
    
    return {"status": "success", "message": "Đã cập nhật ảnh đại diện.", "avatar_url": avatar_url}

# ========================================================
# 8. YÊU CẦU ĐỔI EMAIL (Gửi OTP)
# ========================================================
@router.post("/profile/change-email/request")
async def request_change_email(data: ChangeEmailRequest, auth_data: tuple = Depends(get_current_user_id)):
    user_id, username = auth_data
    cursor = db_manager.connection.cursor()
    
    # Kiểm tra email đã có người dùng chưa
    cursor.execute("SELECT id FROM users WHERE email=%s", (data.new_email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email này đã được sử dụng bởi người khác!")
        
    otp_code = ''.join(random.choices(string.digits, k=6))
    if not send_otp_email(data.new_email, otp_code, username):
        raise HTTPException(status_code=500, detail="Lỗi máy chủ khi gửi Email.")
        
    # Lưu tạm mã OTP vào DB
    cursor.execute("UPDATE users SET otp_code=%s WHERE id=%s", (otp_code, user_id))
    db_manager.connection.commit()
    
    return {"status": "success", "message": "Đã gửi mã OTP đến Email mới."}

# ========================================================
# 9. XÁC NHẬN ĐỔI EMAIL
# ========================================================
@router.post("/profile/change-email/verify")
async def verify_change_email(data: VerifyChangeEmailRequest, auth_data: tuple = Depends(get_current_user_id)):
    user_id, _ = auth_data
    cursor = db_manager.connection.cursor()
    
    cursor.execute("SELECT otp_code FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    
    db_otp = user['otp_code'] if isinstance(user, dict) else user[0]
    
    if not db_otp or db_otp != data.otp:
        raise HTTPException(status_code=400, detail="Mã OTP không chính xác.")
        
    cursor.execute("UPDATE users SET email=%s, otp_code=NULL WHERE id=%s", (data.new_email, user_id))
    db_manager.connection.commit()
    
    return {"status": "success", "message": "Đổi Email thành công!"}