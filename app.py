import os
import json
import re
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from werkzeug.exceptions import BadRequest

# Cấu hình logging chuyên nghiệp
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) # Cho phép Frontend (HTML) gọi API tới Backend

# Lấy API key từ biến môi trường để bảo mật, fallback về key mặc định
API_KEY = os.environ.get("NVIDIA_API_KEY", "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")
MODEL_NAME = os.environ.get("AI_MODEL_NAME", "deepseek-ai/deepseek-v4-pro")

client = OpenAI(
  base_url="https://integrate.api.nvidia.com/v1",
  api_key=API_KEY
)

# --- 3. ĐỊNH NGHĨA CÔNG CỤ (TOOLS) CHO AI TRUY CẬP HỆ THỐNG ---
BASE_DIR = os.environ.get("MEDIA_BASE_DIR", "/sdcard/coder/media")

def list_directory(path="."):
    """Trả về danh sách file và thư mục để AI biết dự án đang có gì"""
    full_path = os.path.abspath(os.path.join(BASE_DIR, path))
    if not full_path.startswith(BASE_DIR):
        return "Lỗi: AI không có quyền truy cập ra ngoài thư mục media."
    try:
        items = os.listdir(full_path)
        return f"Danh sách các mục trong '{path}': " + ", ".join(items)
    except Exception as e:
        logger.error(f"Lỗi khi đọc thư mục {path}: {e}")
        return f"Lỗi khi đọc thư mục: {str(e)}"

def read_file(file_path):
    """Đọc nội dung của một file cụ thể để AI sửa code hoặc tư vấn"""
    full_path = os.path.abspath(os.path.join(BASE_DIR, file_path))
    if not full_path.startswith(BASE_DIR):
        return "Lỗi: AI không có quyền truy cập ra ngoài thư mục media."
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Giới hạn nội dung đọc để tránh quá tải token (khoảng 6000 ký tự)
            if len(content) > 6000:
                return content[:6000] + "\n\n...[Nội dung đã bị cắt bớt do quá dài]..."
            return content
    except Exception as e:
        logger.error(f"Lỗi khi đọc file {file_path}: {e}")
        return f"Lỗi khi đọc file: {str(e)}"

available_tools = {
    "list_directory": list_directory,
    "read_file": read_file
}

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "Xem danh sách các file và thư mục trong dự án để hiểu cấu trúc code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Đường dẫn tương đối (vd: '.', 'TroLyAo.com', 'music')"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Đọc nội dung code hoặc văn bản của một file cụ thể để phân tích và hỗ trợ lập trình.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Đường dẫn file (vd: 'server.py', 'TroLyAo.com/src/brain.js')"}
                },
                "required": ["file_path"]
            }
        }
    }
]

def extract_text_from_ai_response(content):
    """
    Xử lý trường hợp AI trả về chuỗi JSON thô thay vì text.
    """
    if not content:
        return ""
    content = content.strip()
    
    content_to_parse = content
    # Loại bỏ markdown code block json nếu có
    if content.startswith('```json') and content.endswith('```'):
        content_to_parse = content[7:-3].strip()
    
    # Thử parse xem nội dung có phải là JSON object không
    if content_to_parse.startswith('{') and content_to_parse.endswith('}'):
        try:
            data = json.loads(content_to_parse)
            # Các key phổ biến mà AI hay dùng nếu bị nhầm format
            for key in ['response', 'message', 'content', 'reply', 'answer', 'text']:
                if key in data and isinstance(data[key], str):
                    return data[key]
        except Exception:
            pass
            
    return content

SYSTEM_PROMPT = {
    "role": "system", 
    "content": """Bạn là 'Media Hub AI' - Siêu trợ lý lập trình và quản lý dự án nội bộ.
Bạn đang chạy trên môi trường máy chủ Linux tại thư mục '/sdcard/coder/media/'.
Bạn ĐƯỢC CẤP QUYỀN sử dụng các công cụ (tools) để quét thư mục và đọc nội dung file.
Nhiệm vụ của bạn:
1. Đọc, phân tích và hướng dẫn sửa code cho người dùng khi họ yêu cầu.
2. Hướng dẫn người dùng các chức năng như một trợ lý giải trí.
3. Luôn sử dụng tools để đọc file trước khi trả lời nếu người dùng nhắc tới một file cụ thể.
Trả lời bằng tiếng Việt, cực kỳ thông minh, súc tích và chuyên nghiệp như một Senior Developer.
QUAN TRỌNG: Chỉ trả lời bằng văn bản thuần túy hoặc markdown. TUYỆT ĐỐI KHÔNG bọc câu trả lời trong chuỗi JSON (ví dụ: không dùng {"response": "..."})."""
}

# Lưu lịch sử hội thoại theo phiên (session_id) giúp Thread-safe khi có nhiều user truy cập
user_sessions = {}

def get_chat_history(session_id):
    if session_id not in user_sessions:
        user_sessions[session_id] = [SYSTEM_PROMPT.copy()]
    return user_sessions[session_id]

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            raise BadRequest("Nội dung 'message' không được trống")
            
        user_message = data['message']
        session_id = data.get('session_id', 'default_user')
        
        chat_history = get_chat_history(session_id)
        chat_history.append({"role": "user", "content": user_message})

        # Giữ lại 1 system prompt và 14 tin nhắn gần nhất để tối ưu token
        if len(chat_history) > 15:
            chat_history[:] = [chat_history[0]] + chat_history[-14:]

        logger.info(f"Đang gửi request tới AI model {MODEL_NAME}...")
        
        MAX_TURNS = 5
        turn = 0
        
        while turn < MAX_TURNS:
            turn += 1
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=chat_history,
                temperature=0.7,
                tools=tools_schema,
                tool_choice="auto",
                max_tokens=2000,
                timeout=360 # Giới hạn thời gian kết nối (Tăng lên 120s để xử lý các câu lệnh dài không bị lỗi)
            )
            
            message = response.choices[0].message
            content = message.content or ""

            if message.tool_calls:
                logger.info(f"AI yêu cầu gọi {len(message.tool_calls)} tools (vòng {turn}).")
                # Pydantic model_dump là chuẩn chỉnh nhất để đưa tin nhắn tool về dict
                chat_history.append(message.model_dump(exclude_none=True))
                
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    try:
                        function_args = json.loads(tool_call.function.arguments)
                    except Exception:
                        function_args = {}
                    
                    function_to_call = available_tools.get(function_name)
                    if function_to_call:
                        function_response = function_to_call(**function_args)
                    else:
                        function_response = f"Lỗi: Không tìm thấy công cụ '{function_name}'"
                    
                    chat_history.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(function_response),
                    })
                continue # Tiếp tục vòng lặp để AI xử lý kết quả
                
            elif "DSML" in content and ("invoke" in content or "tool_calls" in content):
                logger.info(f"AI trả về format DSML (vòng {turn}), tiến hành parse...")
                chat_history.append({"role": "assistant", "content": content})
                
                # Giải mã HTML entities nếu AI trả về &lt; thay vì <
                content_decoded = content.replace('&lt;', '<').replace('&gt;', '>')
                invokes = list(re.finditer(r'<[|｜]DSML[|｜]invoke\s+name="([^"]+)"[^>]*>(.*?)</[|｜]DSML[|｜]invoke>', content_decoded, re.DOTALL))
                
                if invokes:
                    for invoke in invokes:
                        function_name = invoke.group(1)
                        params_str = invoke.group(2)
                        
                        args = {}
                        param_matches = re.finditer(r'<[|｜]DSML[|｜]parameter\s+name="([^"]+)"[^>]*>(.*?)</[|｜]DSML[|｜]parameter>', params_str, re.DOTALL)
                        for p in param_matches:
                            args[p.group(1)] = p.group(2).strip()
                            
                        function_to_call = available_tools.get(function_name)
                        if function_to_call:
                            function_response = function_to_call(**args)
                            chat_history.append({
                                "role": "user",
                                "content": f"<|DSML|result>\n{function_response}\n</|DSML|result>"
                            })
                        else:
                            chat_history.append({
                                "role": "user",
                                "content": f"<|DSML|result>\nLỗi: Không tìm thấy công cụ '{function_name}'\n</|DSML|result>"
                            })
                    continue # Tiếp tục vòng lặp sau khi nạp kết quả
                
            # Xử lý text cuối cùng
            final_reply = extract_text_from_ai_response(content)
            
            # Xóa các thẻ DSML thô còn sót lại rác
            final_reply = re.sub(r'&lt;[|｜]DSML[|｜].*?&gt;.*?&lt;/[|｜]DSML[|｜].*?&gt;', '', final_reply, flags=re.DOTALL)
            final_reply = re.sub(r'&lt;[|｜]DSML[|｜].*?&gt;', '', final_reply)
            final_reply = re.sub(r'<[|｜]DSML[|｜].*?>.*?</[|｜]DSML[|｜].*?>', '', final_reply, flags=re.DOTALL)
            final_reply = re.sub(r'<[|｜]DSML[|｜].*?>', '', final_reply)
            final_reply = final_reply.strip()
            
            if not final_reply and turn < MAX_TURNS:
                chat_history.append({"role": "user", "content": "Vui lòng trả lời bằng văn bản thông thường, không dùng định dạng gọi hàm thô."})
                continue
                
            if not final_reply:
                final_reply = "Đã xử lý xong nhưng không thể hiển thị kết quả do lỗi định dạng."
                
            chat_history.append({"role": "assistant", "content": final_reply})
            return jsonify({"response": final_reply})
            
        return jsonify({"response": "Lỗi: Quá trình xử lý của AI bị lặp vô hạn."})

    except BadRequest as e:
        logger.warning(f"Bad Request: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Lỗi Server: {e}", exc_info=True)
        return jsonify({"error": "Đã xảy ra lỗi trong quá trình xử lý. Vui lòng thử lại sau."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1414, threaded=True, debug=False)
