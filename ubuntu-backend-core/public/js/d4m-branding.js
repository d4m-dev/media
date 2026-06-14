// Đóng gói logic vào một hàm để dễ dàng gọi
function applyD4MBranding() {
    // 1. Xử lý chữ cuộn
    let originalTitle = document.title ? document.title.trim() : "Project";
    originalTitle = originalTitle.replace(/[-|•]?\s*d4m-dev\s*/gi, "").trim();
    let scrollingText = ` ${originalTitle} • d4m-dev • `;
    
    setInterval(() => {
        scrollingText = scrollingText.substring(1) + scrollingText.substring(0, 1);
        document.title = scrollingText;
    }, 250);

    // 2. Xử lý Favicon Terminal
    const canvas = document.createElement('canvas');
    canvas.width = 32;
    canvas.height = 32;
    const ctx = canvas.getContext('2d');

    let faviconLink = document.querySelector("link[rel*='icon']");
    if (!faviconLink) {
        faviconLink = document.createElement('link');
        faviconLink.rel = 'shortcut icon';
        document.head.appendChild(faviconLink);
    }

    let cursorVisible = true;
    setInterval(() => {
        ctx.clearRect(0, 0, 32, 32);
        
        ctx.fillStyle = "#111111"; // Nền đen
        ctx.beginPath();
        ctx.arc(16, 16, 16, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#00ff66"; // Chữ xanh
        ctx.font = "bold 20px monospace";
        ctx.fillText(">", 4, 23);

        if (cursorVisible) {
            ctx.fillStyle = "#00ff66";
            ctx.fillRect(18, 8, 10, 14); 
        }
        cursorVisible = !cursorVisible;
        faviconLink.href = canvas.toDataURL('image/png');
    }, 500);
}

// 🚀 KIỂM TRA TRẠNG THÁI: Nếu web chưa load xong thì đợi, nếu load xong rồi thì CHẠY LUÔN!
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applyD4MBranding);
} else {
    applyD4MBranding();
}