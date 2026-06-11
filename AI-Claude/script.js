const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

let messageHistory = [];

function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message');
    msgDiv.classList.add(sender === 'user' ? 'user-message' : 'ai-message');
    msgDiv.textContent = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const text = userInput.value.trim();

    if (!text) return;

    // Hiển thị tin nhắn người dùng
    appendMessage('user', text);
    userInput.value = '';

    // Cập nhật mảng lịch sử trò chuyện
    messageHistory.push({ role: 'user', content: text });

    // Hiển thị trạng thái đang tải
    const loadingDiv = document.createElement('div');
    loadingDiv.classList.add('message', 'ai-message', 'loading');
    loadingDiv.textContent = 'AI đang phân tích...';
    chatBox.appendChild(loadingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        // Gọi API thông qua Backend app.py để tránh lỗi CORS
        const response = await fetch('http://192.168.110.2:1414/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: text
            })
        });

        chatBox.removeChild(loadingDiv);

        if (!response.ok) {
            const err = await response.json();
            appendMessage('ai', 'Đã xảy ra lỗi: ' + (err.error || response.statusText));
            return;
        }

        const data = await response.json();
        const aiText = data.response; // Dữ liệu trả về từ Backend
        
        appendMessage('ai', aiText);
        // Lưu tin nhắn của AI vào lịch sử để duy trì ngữ cảnh
        messageHistory.push({ role: 'assistant', content: aiText });

    } catch (error) {
        chatBox.removeChild(loadingDiv);
        appendMessage('ai', 'Lỗi kết nối mạng: ' + error.message);
    }
}

sendBtn.addEventListener('click', sendMessage);

// Lắng nghe sự kiện nhấn Enter để gửi tin nhắn (Shift+Enter để xuống dòng)
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});