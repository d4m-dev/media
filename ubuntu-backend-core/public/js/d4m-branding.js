// ============================================================
// 🌐 D4M-DEV GLOBAL SYSTEM: BRANDING & GLOBAL TOAST NOTIFICATION
// ============================================================

(function() {
    // ---------------------------------------------------------
    // 1. HỆ THỐNG GIAO DIỆN TOAST (GLASSMORPHISM) KHÔNG CẦN TAILWIND
    // ---------------------------------------------------------
    const style = document.createElement('style');
    style.innerHTML = `
        #d4m-toast-container { position: fixed; top: 20px; right: 20px; display: flex; flex-direction: column; gap: 12px; z-index: 999999; pointer-events: none; }
        .d4m-glass-toast { 
            background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(239, 68, 68, 0.15);
            padding: 16px; width: 320px; display: flex; align-items: flex-start; gap: 16px;
            transform: translateX(120%); transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            pointer-events: auto; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; position: relative; overflow: hidden;
        }
        .d4m-glass-toast.show { transform: translateX(0); }
        .d4m-toast-icon { filter: drop-shadow(0 0 8px rgba(239, 68, 68, 0.8)); margin-top: 2px; }
        .d4m-toast-title { margin: 0 0 4px 0; font-weight: bold; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; }
        .d4m-toast-msg { margin: 0; font-size: 12px; color: #d1d5db; line-height: 1.5; }
        .d4m-toast-bar-wrapper { position: absolute; bottom: 0; left: 0; width: 100%; height: 3px; }
        .d4m-toast-bar { height: 100%; background: linear-gradient(90deg, #ef4444, #f97316); animation: d4mShrink 5s linear forwards; }
        @keyframes d4mShrink { from { width: 100%; } to { width: 0%; } }
    `;
    document.head.appendChild(style);

    // Hàm gọi thông báo toàn cầu (có thể gọi ở bất kỳ đâu)
    window.showGlobalToast = function(title, message, type = "error") {
        let container = document.getElementById('d4m-toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'd4m-toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        const iconSvg = `<svg style="width:24px;height:24px;color:#ef4444;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>`;

        toast.className = 'd4m-glass-toast';
        toast.innerHTML = `
            <div class="d4m-toast-icon">${iconSvg}</div>
            <div style="flex: 1;">
                <h4 class="d4m-toast-title">${title}</h4>
                <p class="d4m-toast-msg">${message}</p>
            </div>
            <div class="d4m-toast-bar-wrapper"><div class="d4m-toast-bar"></div></div>
        `;

        container.appendChild(toast);
        setTimeout(() => toast.classList.add('show'), 10);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 400);
        }, 5000);
    };

    // ---------------------------------------------------------
    // 2. RADAR ĐÁNH CHẶN API (GLOBAL FETCH INTERCEPTOR)
    // ---------------------------------------------------------
    const originalFetch = window.fetch;
    window.fetch = async function(...args) {
        try {
            const response = await originalFetch(...args);
            // Kích hoạt ngay lập tức nếu Server trả về mã 429 (Rate Limit)
            if (response.status === 429) {
                const clonedRes = response.clone();
                clonedRes.json().then(data => {
                    if (data && data.error) {
                        window.showGlobalToast(data.error.title, data.error.message);
                    } else {
                        window.showGlobalToast("Quá Tải Máy Chủ", "Vui lòng thao tác chậm lại!");
                    }
                }).catch(() => {
                    window.showGlobalToast("Cảnh Báo Hệ Thống", "Quá nhiều yêu cầu, vui lòng chờ ít phút.");
                });
            }
            return response;
        } catch (error) {
            throw error;
        }
    };

    // ---------------------------------------------------------
    // 3. HIỆU ỨNG NHẬN DIỆN THƯƠNG HIỆU (CŨ)
    // ---------------------------------------------------------
    function applyD4MBranding() {
        let originalTitle = document.title ? document.title.trim() : "Project";
        originalTitle = originalTitle.replace(/[-|•]?\s*d4m-dev\s*/gi, "").trim();
        let scrollingText = ` ${originalTitle} • d4m-dev • `;
        
        setInterval(() => {
            scrollingText = scrollingText.substring(1) + scrollingText.substring(0, 1);
            document.title = scrollingText;
        }, 250);

        const canvas = document.createElement('canvas');
        canvas.width = 32; canvas.height = 32;
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
            ctx.fillStyle = "#111111"; ctx.beginPath(); ctx.arc(16, 16, 16, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = "#00ff66"; ctx.font = "bold 20px monospace"; ctx.fillText(">", 4, 23);
            if (cursorVisible) { ctx.fillStyle = "#00ff66"; ctx.fillRect(18, 8, 10, 14); }
            cursorVisible = !cursorVisible;
            faviconLink.href = canvas.toDataURL('image/png');
        }, 500);
    }

    // Kích hoạt khi trang đã tải xong
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", applyD4MBranding);
    } else {
        applyD4MBranding();
    }
})();