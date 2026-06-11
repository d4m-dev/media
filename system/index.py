from flask import Flask, jsonify, render_template_string
import psutil
import subprocess
import socket

app = Flask(__name__)

# KHỞI TẠO CPU: Gọi một lần lúc khởi động để psutil có cột mốc so sánh
psutil.cpu_percent(interval=None)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Termux Control Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: linear-gradient(135deg, #0f172a, #3b0764); min-height: 100vh; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .glass { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5); }
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); border-radius: 4px; }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 4px; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-6xl mx-auto">
        <h1 class="text-3xl md:text-4xl font-bold mb-8 text-center bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400 drop-shadow-lg">
            🚀 Termux Control Center
        </h1>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="glass rounded-2xl p-6 flex flex-col justify-center">
                <h2 class="text-xl font-semibold mb-6 border-b border-gray-400/20 pb-3 flex items-center">
                    <span class="mr-2">📊</span> Tài nguyên hệ thống (S26 Ultra)
                </h2>
                
                <div class="mb-5">
                    <div class="flex justify-between mb-2 text-sm text-gray-300">
                        <span>CPU Usage</span>
                        <span id="cpu-text" class="font-bold text-white">0%</span>
                    </div>
                    <div class="w-full bg-gray-800/50 rounded-full h-3 overflow-hidden border border-gray-600/30">
                        <div id="cpu-bar" class="bg-gradient-to-r from-green-400 to-blue-500 h-3 rounded-full transition-all duration-300 ease-out" style="width: 0%"></div>
                    </div>
                </div>

                <div class="mb-5">
                    <div class="flex justify-between mb-2 text-sm text-gray-300">
                        <span>Physical RAM (Hardware) <span id="ram-detail" class="text-purple-300 ml-1">0 / 12 GB</span></span>
                        <span id="ram-text" class="font-bold text-white">0%</span>
                    </div>
                    <div class="w-full bg-gray-800/50 rounded-full h-3 overflow-hidden border border-gray-600/30">
                        <div id="ram-bar" class="bg-gradient-to-r from-purple-400 to-pink-500 h-3 rounded-full transition-all duration-300 ease-out" style="width: 0%"></div>
                    </div>
                </div>

                <div>
                    <div class="flex justify-between mb-2 text-sm text-gray-300">
                        <span>RAM Plus (Swap) <span id="swap-detail" class="text-yellow-300 ml-1">0 / 8 GB</span></span>
                        <span id="swap-text" class="font-bold text-white">0%</span>
                    </div>
                    <div class="w-full bg-gray-800/50 rounded-full h-3 overflow-hidden border border-gray-600/30">
                        <div id="swap-bar" class="bg-gradient-to-r from-yellow-400 to-orange-500 h-3 rounded-full transition-all duration-300 ease-out" style="width: 0%"></div>
                    </div>
                </div>
            </div>

            <div class="glass rounded-2xl p-6 flex flex-col h-96">
                <h2 class="text-xl font-semibold mb-4 border-b border-gray-400/20 pb-3 flex items-center justify-between">
                    <div><span class="mr-2">🌐</span> Active Local Ports</div>
                    <span class="text-xs font-normal px-2 py-1 bg-green-500/20 text-green-300 rounded-full" id="port-count">0 connected</span>
                </h2>
                
                <div class="overflow-y-auto pr-2 flex-1">
                    <table class="w-full text-left border-collapse">
                        <thead class="sticky top-0 bg-[#1e2338] shadow-md z-10">
                            <tr class="text-gray-400 text-xs uppercase tracking-wider">
                                <th class="py-3 px-2 font-medium">Port</th>
                                <th class="py-3 px-2 font-medium">Trạng thái</th>
                                <th class="py-3 px-2 font-medium">Dịch vụ (Dự đoán)</th>
                            </tr>
                        </thead>
                        <tbody id="ports-table" class="text-sm divide-y divide-gray-700/50">
                            <tr><td colspan="3" class="py-4 text-center text-gray-500">Đang quét hệ thống...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        const basePath = window.location.pathname.endsWith('/') 
                         ? window.location.pathname 
                         : window.location.pathname + '/';
        const apiPath = basePath + 'api/stats';

        // Các port dev phổ biến để gán tên hiển thị cho đẹp
        const portNames = {
            25151: "Main Proxy Server",
            25152: "AI ChatBox Server",
            1515: "Web Project (Tailwind/Flask)",
            8080: "Code-Server (VSCode Web)",
            1212: "phpMyAdmin",
            3306: "MySQL / MariaDB",
            8000: "Flask Dashboard"
        };

        async function fetchSystemStats() {
            try {
                const response = await fetch(apiPath);
                const data = await response.json();
                
                // --- UPDATE CPU ---
                document.getElementById('cpu-text').innerText = `${data.cpu}%`;
                document.getElementById('cpu-bar').style.width = `${data.cpu}%`;
                const cpuBar = document.getElementById('cpu-bar');
                if(data.cpu > 80) { cpuBar.className = "bg-gradient-to-r from-orange-400 to-red-500 h-3 rounded-full transition-all duration-300 ease-out"; }
                else { cpuBar.className = "bg-gradient-to-r from-green-400 to-blue-500 h-3 rounded-full transition-all duration-300 ease-out"; }

                // --- UPDATE PHYSICAL RAM (12GB) ---
                document.getElementById('ram-text').innerText = `${data.ram_percent}%`;
                document.getElementById('ram-bar').style.width = `${data.ram_percent}%`;
                // Làm tròn hiển thị theo thực tế Android cấp cho môi trường
                document.getElementById('ram-detail').innerText = `${data.ram_used} / ${data.ram_total} GB`;

                // --- UPDATE RAM PLUS / SWAP (8GB) ---
                document.getElementById('swap-text').innerText = `${data.swap_percent}%`;
                document.getElementById('swap-bar').style.width = `${data.swap_percent}%`;
                document.getElementById('swap-detail').innerText = `${data.swap_used} / ${data.swap_total} GB`;

                // --- UPDATE PORTS ---
                const tableBody = document.getElementById('ports-table');
                tableBody.innerHTML = '';
                
                const sortedPorts = data.ports.sort((a, b) => a.port - b.port);
                document.getElementById('port-count').innerText = `${sortedPorts.length} Listening`;

                if (sortedPorts.length === 0) {
                    tableBody.innerHTML = '<tr><td colspan="3" class="py-4 text-center text-gray-500">Không tìm thấy port nào đang mở.</td></tr>';
                }

                sortedPorts.forEach(p => {
                    const tr = document.createElement('tr');
                    tr.className = "hover:bg-white/5 transition-colors group";
                    
                    let portColor = "text-blue-300";
                    let procName = portNames[p.port] || "Dịch vụ hệ thống";

                    // Đổi màu cho nổi bật các port quan trọng
                    if([25151, 8080, 1515, 1212].includes(p.port)) {
                        portColor = "text-green-400 font-bold drop-shadow-[0_0_2px_rgba(74,222,128,0.8)]";
                    }
                    
                    tr.innerHTML = `
                        <td class="py-2 px-2 font-mono ${portColor}">:${p.port}</td>
                        <td class="py-2 px-2 text-green-400 flex items-center"><span class="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></span> Hoạt động</td>
                        <td class="py-2 px-2 text-gray-200">${procName}</td>
                    `;
                    tableBody.appendChild(tr);
                });
            } catch (error) {
                console.error("Lỗi kết nối API:", error);
            }
        }

        // Chạy ngay lần đầu và giãn cách 2 giây mỗi lần cập nhật
        fetchSystemStats();
        setInterval(fetchSystemStats, 2000);
    </script>
</body>
</html>
"""

def scan_ports_via_socket():
    """
    Hack vượt tường lửa Android: Dùng socket nội bộ gõ cửa từng port thay vì hỏi hệ điều hành.
    Nếu gõ cửa được (mã trả về 0) -> Port đó đang mở.
    """
    # Danh sách các port mà lập trình viên hay dùng, bạn có thể tự thêm bớt ở đây
    common_ports = [80, 443, 1212, 1515, 3000, 3306, 5000, 5173, 8000, 8080, 8081, 9000, 25151, 25152]
    open_ports = []
    
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.05) # Thời gian chờ cực ngắn để không làm lag server
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            open_ports.append({"port": port})
        sock.close()
        
    return open_ports

@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats')
def get_stats():
    # 1. Quét CPU: Đã cấu hình khởi tạo ở đầu file, ép đo trong 0.1s
    cpu = psutil.cpu_percent(interval=0.1)
    
    # 2. Quét RAM Vật lý (Hardware)
    vm = psutil.virtual_memory()
    
    # 3. Quét RAM Plus (Swap Memory)
    sm = psutil.swap_memory()
    
    # 4. Quét Port bằng công cụ Socket Hack
    ports = scan_ports_via_socket()
    
    return jsonify({
        "cpu": cpu,
        "ram_percent": vm.percent,
        "ram_used": round(vm.used / (1024**3), 2),
        "ram_total": round(vm.total / (1024**3), 2),
        "swap_percent": sm.percent,
        "swap_used": round(sm.used / (1024**3), 2),
        "swap_total": round(sm.total / (1024**3), 2),
        "ports": ports
    })

if __name__ == '__main__':
    app.run(debug=True, port=8000)