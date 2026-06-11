#!/usr/bin/env python3
import os
import socket
import subprocess
from pathlib import Path

def get_local_ip():
    """Lấy địa chỉ IP local thực tế (ưu tiên WiFi wlan0)"""
    # Cách 1: Dùng ifconfig để tìm IP của wlan0 (WiFi)
    try:
        result = subprocess.run(['ifconfig'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        current_iface = None
        wlan0_ip = None
        other_ip = None
        
        for line in lines:
            if line and not line.startswith(' '):
                current_iface = line.split(':')[0].strip()
            if 'inet ' in line:
                parts = line.split()
                for i, p in enumerate(parts):
                    if p == 'inet':
                        ip = parts[i+1] if i+1 < len(parts) else ''
                        if ip and not ip.startswith('127.'):
                            # Ưu tiên wlan0
                            if current_iface == 'wlan0':
                                wlan0_ip = ip
                            # Lưu IP khác để fallback
                            elif other_ip is None:
                                other_ip = ip
                        break
        
        # Trả về IP của wlan0 nếu có
        if wlan0_ip:
            return wlan0_ip
        if other_ip:
            return other_ip
    except:
        pass
    
    # Cách 2: Fallback - dùng socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "127.0.0.1"

def generate_project_links():
    # Danh sách các thư mục dự án
    project_dirs = []
    for item in Path('.').iterdir():
        if item.is_dir() and not item.name.startswith('.') and '-beta' not in item.name:
            # Bỏ qua các thư mục không phải là dự án
            if item.name not in ['load-track', 'music', 'ThuVienChinh', '__pycache__']:
                project_dirs.append(item.name)

    # Tạo HTML cho các liên kết - dùng JavaScript để tự động phát hiện host
    links_html = ""
    for project in sorted(project_dirs):
        # Tạo icon ngẫu nhiên cho mỗi dự án
        icons = ["📱", "🎧", "🖼️", "💬", "💰", "🤖", "🎵", "📺", "🎮", "📚"]
        icon = icons[hash(project) % len(icons)]
        links_html += f'            <li class="project-card" data-project-name="{project}"><a href="#" onclick="showPreview(getProjectUrl(\'{project}\'), \'{project}\'); return false;">{icon} {project}</a></li>\n'

    return links_html

def main():
    links_html = generate_project_links()
    
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Media Projects Hub - Tổng Quan Dự Án</title>
    <link rel="apple-touch-icon" sizes="180x180" href="ThuVienChinh/favicon/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="ThuVienChinh/favicon/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="ThuVienChinh/favicon/favicon-16x16.png">
    <link rel="manifest" href="ThuVienChinh/favicon/site.webmanifest">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(45deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            margin: 0;
            padding: 10px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: flex-start;
        }}
        
        @keyframes gradientBG {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        .container {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
            padding: 25px;
            width: 100%;
            max-width: 1400px;
            margin-top: 20px;
            position: relative;
            display: grid;
            grid-template-columns: 1fr 1.2fr;
            grid-template-rows: auto 1fr;
            grid-template-areas: 
                "header header"
                "sidebar preview";
            gap: 20px;
            min-height: 600px;
        }}
        
        .header {{
            grid-area: header;
            text-align: center;
            margin-bottom: 10px;
        }}
        
        .content {{
            position: relative;
            z-index: 1;
            grid-area: sidebar;
            display: flex;
            flex-direction: column;
        }}
        
        .preview-panel {{
            grid-area: preview;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            backdrop-filter: blur(5px);
            min-height: 500px;
            height: fit-content;
            position: sticky;
            top: 20px;
            align-self: start;
            max-height: calc(100vh - 40px);
            overflow-y: auto;
        }}
        
        .preview-content {{
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
        }}
        
        .preview-intro {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 400px;
            text-align: center;
            padding: 20px;
        }}
        
        .preview-frame {{
            width: 100%;
            height: 500px;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 15px;
            display: none;
        }}
        
        .preview-frame.active {{
            display: block;
        }}
        
        .preview-frame iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}
        
        .view-more-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            display: none;
        }}
        
        .view-more-btn.active {{
            display: block;
        }}
        
        .view-more-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
        }}
        
        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.2em;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.1);
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: titleGlow 2s ease-in-out infinite alternate;
        }}
        
        @keyframes titleGlow {{
            from {{ text-shadow: 0 0 10px rgba(255,107,107,0.3); }}
            to {{ text-shadow: 0 0 20px rgba(78, 205, 196, 0.5); }}
        }}
        
        .subtitle {{
            color: #7f8c8d;
            margin-bottom: 25px;
            font-size: 1.1em;
            font-weight: 300;
        }}
        
        .ip-info {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            color: white;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            animation: float 3s ease-in-out infinite;
        }}
        
        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-8px); }}
            100% {{ transform: translateY(0px); }}
        }}
        
        .ip-info strong {{
            display: block;
            margin-bottom: 5px;
            font-size: 1em;
        }}
        
        .highlight {{
            background: rgba(255, 255, 255, 0.2);
            padding: 3px 8px;
            border-radius: 6px;
            font-weight: 600;
            display: inline-block;
            margin-top: 3px;
        }}
        
        .projects-header {{
            margin: 25px 0 15px;
            color: #2c3e50;
            font-size: 1.6em;
            position: relative;
        }}
        
        .projects-header::after {{
            content: '';
            display: block;
            width: 50px;
            height: 3px;
            background: linear-gradient(to right, #ff6b6b, #4ecdc4);
            margin: 8px auto;
            border-radius: 2px;
        }}
        
        .projects-list {{
            list-style: none;
            padding: 0;
            margin: 20px 0;
            display: flex;
            flex-direction: column;
            gap: 12px;
            flex-grow: 1;
        }}
        
        .project-card {{
            margin: 8px 0;
            padding: 15px;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 10px;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            text-align: left;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(0, 0, 0, 0.05);
            cursor: pointer;
        }}
        
        .project-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .project-card:hover {{
            transform: translateY(-5px) scale(1.01);
            box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
            border-color: rgba(102, 126, 234, 0.3);
        }}
        
        .project-card:hover::before {{
            opacity: 1;
        }}
        
        .project-card a {{
            display: block;
            color: #2c3e50;
            text-decoration: none;
            font-size: 1.1em;
            font-weight: 500;
            padding: 10px;
            position: relative;
            z-index: 1;
            transition: color 0.3s ease;
        }}
        
        .project-card a:hover {{
            color: #667eea;
        }}
        
        .footer {{
            margin-top: 30px;
            color: #7f8c8d;
            font-size: 0.9em;
            line-height: 1.5;
        }}
        
        .footer p {{
            margin: 6px 0;
        }}
        
        .pulse {{
            display: inline-block;
            animation: pulse 1.5s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
            100% {{ transform: scale(1); }}
        }}
        
        /* Modal cho màn hình nhỏ */
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(5px);
        }}
        
        .modal-content {{
            background-color: white;
            margin: 8px auto;
            padding: 20px;
            border-radius: 12px;
            width: calc(100% - 16px);
            max-width: calc(100% - 16px);
            max-height: calc(100vh - 60px); /* Giảm 15px so với trước */
            height: calc(100vh - 60px); /* Giảm 15px so với trước */
            position: relative;
            display: flex;
            flex-direction: column;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }}
        
        .modal-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .modal-preview-frame {{
            flex: 1;
            width: 100%;
            min-height: 0; /* Cho phép co lại khi cần */
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 15px;
        }}
        
        .modal-footer {{
            display: flex;
            justify-content: center;
            margin-top: auto;
        }}
        
        .close {{
            color: #aaa;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            z-index: 1001;
        }}
        
        .close:hover,
        .close:focus {{
            color: black;
        }}
        
        .modal-preview-frame iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}
        
        .modal-view-more-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            display: block;
            width: 100%;
            max-width: 200px;
        }}
        
        .modal-view-more-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
        }}
        
        /* Responsive cho màn hình nhỏ */
        @media (max-width: 1024px) {{
            .container {{
                grid-template-columns: 1fr;
                grid-template-areas: 
                    "header"
                    "sidebar";
                min-height: auto;
            }}
            
            .preview-panel {{
                display: none; /* Ẩn panel xem trước trên màn hình nhỏ */
            }}
            
            .content {{
                max-width: 100%;
                padding-right: 0;
            }}
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 5px;
            }}
            
            .container {{
                padding: 20px;
                margin: 10px;
                border-radius: 12px;
            }}
            
            h1 {{
                font-size: 1.8em;
            }}
            
            .subtitle {{
                font-size: 1em;
            }}
            
            .projects-header {{
                font-size: 1.4em;
            }}
            
            .project-card a {{
                font-size: 1em;
                padding: 8px;
            }}
            
            .ip-info {{
                padding: 12px;
            }}
            
            .footer {{
                font-size: 0.85em;
            }}
        }}
        
        @media (max-width: 480px) {{
            body {{
                padding: 3px;
            }}
            
            .container {{
                margin: 5px;
                padding: 15px;
            }}
            
            h1 {{
                font-size: 1.6em;
            }}
            
            .projects-header {{
                font-size: 1.3em;
            }}
            
            .project-card {{
                padding: 12px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><span class="pulse">🎮</span> Media Projects Hub</h1>
            <div class="subtitle">Trung tâm quản lý và truy cập các dự án trong thư mục media</div>
            
            <div class="ip-info">
                <strong>🌐 Truy cập bằng:</strong>
                <div class="highlight" id="current-ip">Đang phát hiện...</div>
                <strong>🔌 Port:</strong>
                <div class="highlight">1515</div>
                <strong>🔗 Cách truy cập:</strong>
                <div class="highlight" id="access-note">Nhấp vào từng dự án bên dưới để mở</div>
            </div>
        </div>
        
        <div class="content">
            <h2 class="projects-header">📋 Danh Sách Dự Án</h2>
            <ul class="projects-list">
{links_html}
            </ul>
            
            <div class="footer">
                <p>💡 <strong>Lưu ý:</strong> Các liên kết sẽ mở dự án tương ứng trên máy chủ local.</p>
                <p>🔧 Được tạo tự động từ thư mục media hiện tại.</p>
                <p>📱 Giao diện tối ưu cho thiết bị di động</p>
            </div>
        </div>
        
        <div class="preview-panel" id="previewPanel">
            <div class="preview-content">
                <div class="preview-intro" id="previewIntro">
                    <h3>👋 Xin chào!</h3>
                    <p>Chọn một dự án từ danh sách bên trái để xem bản xem trước ở đây.</p>
                    <p>Panel này sẽ hiển thị nội dung trực tiếp của dự án bạn chọn.</p>
                    <div style="margin-top: 20px; font-size: 2em;">📱</div>
                </div>
                <div class="preview-frame" id="previewFrameContainer">
                    <iframe id="previewFrame" src="about:blank"></iframe>
                </div>
                <button class="view-more-btn" id="viewMoreBtn">Xem Thêm</button>
            </div>
        </div>
    </div>
    
    <!-- Modal cho màn hình nhỏ -->
    <div id="previewModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 id="modalPreviewTitle">Xem trước dự án</h3>
                <span class="close">&times;</span>
            </div>
            <div class="modal-preview-frame">
                <iframe id="modalPreviewFrame" src="about:blank"></iframe>
            </div>
            <div class="modal-footer">
                <button class="modal-view-more-btn" id="modalViewMoreBtn">Xem Thêm</button>
            </div>
        </div>
    </div>
    
    <script>
        // Hàm lấy URL hiện tại của host (IP hoặc Cloudflare)
        function getBaseUrl() {{
            const protocol = window.location.protocol;
            const hostname = window.location.hostname;
            const port = window.location.port;
            
            // Nếu là localhost hoặc IP - luôn hiện port
            const ipRegex = /^\\d+\\.\\d+\\.\\d+\\.\\d+$/;
            if (hostname === 'localhost' || hostname === '127.0.0.1' || ipRegex.test(hostname)) {{
                return protocol + '//' + hostname + ':' + (port || '1515');
            }}
            // Nếu là domain (cloudflare) - không hiện port (https mặc định 443)
            else {{
                return protocol + '//' + hostname;
            }}
        }}
        
        // Hàm hiển thị IP/hostname hiện tại
        function displayCurrentIp() {{
            const ipDisplay = document.getElementById('current-ip');
            const accessNote = document.getElementById('access-note');
            const hostname = window.location.hostname;
            const port = window.location.port || (window.location.protocol === 'https:' ? '443' : '80');
            const protocol = window.location.protocol;
            
            // Kiểm tra loại kết nối
            if (hostname === 'localhost' || hostname === '127.0.0.1') {{
                // Localhost
                ipDisplay.textContent = 'localhost:' + port;
                ipDisplay.style.background = 'rgba(102, 126, 234, 0.3)';
                accessNote.textContent = '📱 Bạn đang truy cập từ máy này';
            }} else if (/^\\d+\\.\\d+\\.\\d+\\.\\d+$/.test(hostname)) {{
                // IP local (WiFi) - có port
                ipDisplay.textContent = hostname + ':' + port;
                ipDisplay.style.background = 'rgba(78, 205, 196, 0.3)';
                accessNote.textContent = '📶 Bạn đang truy cập qua mạng WiFi nội bộ';
            }} else {{
                // Domain (Cloudflare) - không hiện port
                ipDisplay.textContent = hostname;
                ipDisplay.style.background = 'rgba(255, 107, 107, 0.3)';
                accessNote.textContent = '🌍 Bạn đang truy cập từ xa qua Cloudflare Tunnel';
            }}
        }}
        
        // Hàm tạo URL cho dự án
        function getProjectUrl(projectName) {{
            return getBaseUrl() + '/' + projectName + '/';
        }}
        
        // Thêm hiệu ứng động cho các phần tử
        document.addEventListener('DOMContentLoaded', function() {{
            // Hiển thị IP/hostname hiện tại
            displayCurrentIp();
            
            const cards = document.querySelectorAll('.project-card');
            cards.forEach(function(card, index) {{
                card.style.opacity = '0';
                card.style.transform = 'translateY(10px)';

                setTimeout(function() {{
                    card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }}, index * 100);
            }});
        }});

        function showPreview(url, projectName) {{
            // Kiểm tra kích thước màn hình
            if (window.innerWidth <= 1024) {{
                // Màn hình nhỏ - sử dụng modal
                const modal = document.getElementById('previewModal');
                const modalPreviewFrame = document.getElementById('modalPreviewFrame');
                const modalPreviewTitle = document.getElementById('modalPreviewTitle');
                const modalViewMoreBtn = document.getElementById('modalViewMoreBtn');
                
                // Cập nhật tiêu đề
                modalPreviewTitle.textContent = 'Xem trước: ' + projectName;
                
                // Cập nhật src của iframe
                modalPreviewFrame.src = url;
                
                // Cập nhật nút "Xem thêm" để mở link
                modalViewMoreBtn.onclick = function() {{
                    window.open(url, '_blank');
                }};
                
                // Hiển thị modal và chặn cuộn trang chính
                modal.style.display = 'block';
                document.body.style.overflow = 'hidden';
            }} else {{
                // Màn hình lớn - sử dụng panel xem trước như trước
                const previewFrame = document.getElementById('previewFrame');
                const previewIntro = document.getElementById('previewIntro');
                const previewFrameContainer = document.getElementById('previewFrameContainer');
                const viewMoreBtn = document.getElementById('viewMoreBtn');

                // Ẩn phần giới thiệu và hiển thị iframe
                previewIntro.style.display = 'none';
                previewFrameContainer.classList.add('active');
                viewMoreBtn.classList.add('active');

                // Cập nhật src của iframe
                previewFrame.src = url;

                // Cập nhật nút "Xem thêm" để mở link
                viewMoreBtn.onclick = function() {{
                    window.open(url, '_blank');
                }};
            }}
        }}
        
        // Đóng modal khi nhấn nút close
        document.querySelector('.close').onclick = function() {{
            document.getElementById('previewModal').style.display = 'none';
            document.body.style.overflow = 'auto'; // Cho phép cuộn lại trang chính
        }}
        
        // Đóng modal khi nhấn ngoài nội dung
        window.onclick = function(event) {{
            const modal = document.getElementById('previewModal');
            if (event.target === modal) {{
                modal.style.display = 'none';
                document.body.style.overflow = 'auto'; // Cho phép cuộn lại trang chính
            }}
        }}
        
        // Đóng modal khi nhấn ESC
        document.addEventListener('keydown', function(event) {{
            if (event.key === 'Escape') {{
                const modal = document.getElementById('previewModal');
                if (modal.style.display === 'block') {{
                    modal.style.display = 'none';
                    document.body.style.overflow = 'auto'; // Cho phép cuộn lại trang chính
                }}
            }}
        }});
    </script>
</body>
</html>"""
    
    print(html_content)

if __name__ == "__main__":
    main()