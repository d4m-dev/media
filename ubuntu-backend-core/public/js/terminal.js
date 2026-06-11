// File: public/js/terminal.js
const WS_URL = "ws://192.168.110.2:16868/ws/logs";
let ws;

function connectWebSocket() {
    ws = new WebSocket(WS_URL);
    const terminalOutput = document.getElementById('terminal-output');

    ws.onopen = () => {
        appendLog('<span class="text-blue-400">✅ Đã kết nối đường truyền. Bắt đầu nhận log...</span>');
    };

    ws.onmessage = (event) => {
        const logMessage = event.data;
        let colorClass = "text-gray-300"; // Mặc định
        
        // Phân loại màu sắc theo mã HTTP trạng thái
        if (logMessage.includes(" 200 ")) colorClass = "text-green-400";
        else if (logMessage.includes(" 404 ") || logMessage.includes(" 403 ") || logMessage.includes(" 422 ")) colorClass = "text-yellow-400";
        else if (logMessage.includes(" 500 ")) colorClass = "text-red-500";
        
        appendLog(`<span class="${colorClass}">${logMessage}</span>`);
    };

    ws.onclose = () => {
        appendLog('<span class="text-red-500">❌ Mất kết nối. Đang thử kết nối lại sau 3s...</span>');
        setTimeout(connectWebSocket, 3000);
    };
}

function appendLog(htmlContent) {
    const terminalOutput = document.getElementById('terminal-output');
    const newLine = document.createElement('div');
    newLine.innerHTML = htmlContent;
    terminalOutput.appendChild(newLine);
    
    // Tự động cuộn xuống dòng mới nhất
    terminalOutput.scrollTop = terminalOutput.scrollHeight;
}

document.addEventListener('DOMContentLoaded', () => {
    connectWebSocket();
});