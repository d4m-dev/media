from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from google import genai 
import re

from core.security import verify_token
from core.config import settings
from core.database import get_raw_logs
from api.dashboard import api_status_db
from scripts.network_tunnel import start_tunnel, stop_tunnel

router = APIRouter(
    prefix="/api/ai-admin",
    tags=["AI Admin"],
    dependencies=[Depends(verify_token)] 
)

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def ai_admin_chat(request: ChatRequest):
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=400, detail="Chưa cấu hình GEMINI_API_KEY trong file .env")

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        # ==========================================
        # 🚀 RADAR TỰ ĐỘNG DÒ TÌM MODEL ĐƯỢC PHÉP DÙNG
        # ==========================================
        available_models = []
        for m in client.models.list():
            if 'gemini' in m.name.lower() and hasattr(m, 'supported_actions') and 'generateContent' in m.supported_actions:
                available_models.append(m.name)
            elif 'gemini' in m.name.lower():
                available_models.append(m.name)
        
        if not available_models:
            raise Exception("Khóa API Key không có quyền truy cập bất kỳ mô hình Gemini nào trên Google Cloud.")

        chosen_model = None
        for target in ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']:
            match_model = next((m for m in available_models if target in m.lower()), None)
            if match_model:
                chosen_model = match_model
                break
                
        if not chosen_model:
            chosen_model = available_models[0]

        clean_model_name = chosen_model.replace('models/', '')

        # ==========================================
        # THU THẬP DỮ LIỆU HỆ THỐNG BIẾN ĐỘNG REALTIME
        # ==========================================
        recent_logs = get_raw_logs(limit=30)
        current_status = "\n".join([f"- {k}: {'ĐANG BẬT' if v['active'] else 'ĐANG TẮT'}" for k, v in api_status_db.items()])

        system_prompt = f"""
        Bạn là AI Quản trị viên (Admin) sở hữu đặc quyền tối cao của hệ thống Ubuntu Backend Core. Ngôn ngữ giao tiếp: Tiếng Việt.
        Nhiệm vụ trọng tâm của bạn là phân tích log truy cập hệ thống để phát hiện bất thường và thực thi chuẩn xác các lệnh hạ tầng từ người chủ.

        Trạng thái vận hành thực tế của các dịch vụ API hiện tại:
        {current_status}

        Bản trích xuất dữ liệu 30 dòng nhật ký hệ thống (Logs) gần nhất:
        {recent_logs}

        QUY TẮC THỰC THI HẠ TẦNG BẮT BUỘC:
        Khi người chủ ra lệnh yêu cầu BẬT hoặc TẮT một dịch vụ cụ thể nằm trong danh sách kiểm soát (bao gồm: internet_tunnel, chatbox_ai, social_db), bạn phải phân tích ngữ cảnh, đưa ra phản hồi ngắn gọn lịch sự và BẮT BUỘC chèn cú pháp mã lệnh kỹ thuật sau đây vào cuối cùng văn bản phản hồi của bạn:
        [TOGGLE: ten_dich_vu]
        Ví dụ minh họa: [TOGGLE: internet_tunnel] hoặc [TOGGLE: chatbox_ai]. Tuyệt đối không chèn thêm bất kỳ ký tự hoặc dấu chấm câu nào phía sau mã này.
        
        Yêu cầu hiện tại từ người chủ hệ thống: {request.message}
        """

        response = client.models.generate_content(
            model=clean_model_name,
            contents=system_prompt,
        )
        reply_text = response.text

        # ==========================================
        # ⚡ PHÂN TÍCH VÀ KÍCH HOẠT QUYỀN ĐIỀU KHIỂN CỐT LÕI
        # ==========================================
        action_taken = None
        match = re.search(r'\[TOGGLE:\s*([a-zA-Z0-9_]+)\]', reply_text)
        
        if match:
            target_service = match.group(1).strip()
            if target_service in api_status_db:
                current_state = api_status_db[target_service]["active"]
                new_state = not current_state
                
                if target_service == "internet_tunnel":
                    if new_state: start_tunnel()
                    else: stop_tunnel()
                
                api_status_db[target_service]["active"] = new_state
                action_taken = f"Hệ thống đã thực thi lệnh: {'BẬT' if new_state else 'TẮT'} thành công dịch vụ {target_service}"
                reply_text = re.sub(r'\[TOGGLE:\s*([a-zA-Z0-9_]+)\]', '', reply_text).strip()

        return {
            "status": "success",
            "reply": reply_text,
            "action_executed": action_taken,
            "debug_model": clean_model_name
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống AI: {str(e)}")