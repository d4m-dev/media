from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.security import verify_password, create_access_token, ADMIN_USERNAME

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(request: LoginRequest):
    # Kiểm tra tài khoản và mật khẩu
    if request.username != ADMIN_USERNAME or not verify_password(request.password):
        raise HTTPException(status_code=401, detail="❌ Sai tên đăng nhập hoặc mật khẩu!")
    
    # Tạo Token
    access_token = create_access_token(data={"sub": request.username, "role": "admin"})
    
    return {
        "status": "success",
        "message": "✅ Đăng nhập thành công!",
        "access_token": access_token,
        "token_type": "bearer"
    }