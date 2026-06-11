// URL của Backend Core (Nếu bạn truy cập từ nơi khác, có thể đổi thành IP tương ứng)
const API_BASE_URL = "http://192.168.110.2:16868/api";

let authToken = localStorage.getItem("backend_token");
let statInterval;

// ==========================================
// 1. CÁC HÀM TIỆN ÍCH & GIAO DIỆN
// ==========================================

// Hàm Copy to Clipboard siêu tốc kèm hiệu ứng Tick xanh
window.copyToClipboard = async function(text, btnElement) {
    try {
        await navigator.clipboard.writeText(text);
        
        // Lưu lại icon cũ
        const originalHTML = btnElement.innerHTML;
        
        // Chuyển sang hiệu ứng Tick xanh
        btnElement.innerHTML = '<i class="fa-solid fa-check text-green-400 scale-125 transition-transform duration-200"></i>';
        
        // Trả lại icon cũ sau 2 giây
        setTimeout(() => {
            btnElement.innerHTML = originalHTML; 
        }, 2000);
    } catch(e) {
        console.error("Lỗi khi copy:", e);
    }
}

// ==========================================
// 2. HỆ THỐNG XÁC THỰC (JWT AUTHENTICATION)
// ==========================================

// Kiểm tra quyền truy cập khi tải trang
function checkAuth() {
    if (!authToken) {
        document.getElementById('login-overlay').classList.remove('hidden');
        clearInterval(statInterval); // Dừng cập nhật dữ liệu nếu chưa đăng nhập
    } else {
        document.getElementById('login-overlay').classList.add('hidden');
        // Nếu có Token hợp lệ, bắt đầu lấy dữ liệu hiển thị
        fetchSystemStats();
        fetchServices();
        
        // Bật tự động cập nhật phần cứng mỗi 2 giây
        statInterval = setInterval(fetchSystemStats, 2000);
    }
}

// Xử lý sự kiện khi bấm nút Đăng Nhập
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const usernameVal = document.getElementById('username').value;
    const passwordVal = document.getElementById('password').value;
    const errorDiv = document.getElementById('login-error');
    const spinner = document.getElementById('login-spinner');
    
    spinner.classList.remove('hidden');
    errorDiv.classList.add('hidden');

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: usernameVal, password: passwordVal })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Đăng nhập thành công, lưu Chìa khóa (Token) vào trình duyệt
            authToken = data.access_token;
            localStorage.setItem("backend_token", authToken);
            checkAuth(); // Cập nhật lại Giao diện để ẩn form đăng nhập
        } else {
            errorDiv.innerText = data.detail || "Sai tài khoản hoặc mật khẩu!";
            errorDiv.classList.remove('hidden');
        }
    } catch (error) {
        errorDiv.innerText = "Không thể kết nối đến máy chủ Backend!";
        errorDiv.classList.remove('hidden');
    } finally {
        spinner.classList.add('hidden');
    }
});

// Hàm Đăng Xuất
function logout() {
    localStorage.removeItem("backend_token");
    authToken = null;
    checkAuth(); // Gọi lại hàm check để hiện form đăng nhập
}

// Hàm fetch dữ liệu đính kèm Thẻ bảo mật Token
async function fetchWithAuth(url, options = {}) {
    if (!options.headers) options.headers = {};
    options.headers['Authorization'] = `Bearer ${authToken}`; // Gắn chìa khóa vào Header
    
    const response = await fetch(url, options);
    
    // Nếu token hết hạn hoặc cố tình chỉnh sửa sai, bắt đăng nhập lại ngay
    if (response.status === 401) {
        logout();
        throw new Error("Token hết hạn hoặc không hợp lệ");
    }
    return response;
}

// ==========================================
// 3. XỬ LÝ DỮ LIỆU BẢNG ĐIỀU KHIỂN (DASHBOARD)
// ==========================================

// Lấy thông số phần cứng (CPU, RAM, Ổ cứng)
async function fetchSystemStats() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/dashboard/system-stats`);
        const data = await response.json();

        document.getElementById('cpu-val').innerText = `${data.cpu_usage_percent}%`;
        document.getElementById('ram-val').innerText = `${data.ram.percent}%`;
        document.getElementById('ram-detail').innerText = `${data.ram.used_gb} / ${data.ram.total_gb} GB`;
        document.getElementById('disk-val').innerText = `${data.storage.percent}%`;
        document.getElementById('disk-detail').innerText = `Free: ${data.storage.free_gb} GB`;
    } catch (error) {
        console.error("Lỗi lấy thông số phần cứng:", error);
    }
}

// Lấy danh sách API Services và Render ra màn hình
async function fetchServices() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/dashboard/services`);
        const data = await response.json();
        const container = document.getElementById('services-container');
        container.innerHTML = ''; // Xóa bộ khung skeleton loading

        for (const [serviceName, info] of Object.entries(data.services)) {
            const isChecked = info.active ? 'checked' : '';
            
            // Xử lý khối giao diện in ra đường Link public nếu dịch vụ đang bật và có link
            let linkHtml = '';
            if (info.active && info.public_url) {
                linkHtml = `
                    <div class="mt-2 text-sm bg-black/40 py-1.5 px-3 rounded-lg inline-flex items-center border border-green-500/30 group">
                        <i class="fa-solid fa-link text-green-400 mr-2"></i>
                        <a href="${info.public_url}" target="_blank" class="text-green-400 hover:text-green-300 font-mono tracking-wide mr-3">${info.public_url}</a>
                        <button onclick="copyToClipboard('${info.public_url}', this)" class="text-gray-400 hover:text-white transition-colors p-1" title="Copy Link">
                            <i class="fa-regular fa-copy"></i>
                        </button>
                    </div>
                `;
            }

            // Xây dựng thẻ HTML cho từng dịch vụ
            const html = `
                <div class="flex justify-between items-center p-3 rounded-xl bg-white/5 hover:bg-white/10 transition">
                    <div class="flex-1 pr-4">
                        <h4 class="font-medium text-blue-300 capitalize">${serviceName.replace(/_/g, ' ')}</h4>
                        <p class="text-xs text-gray-400 mt-1">${info.description}</p>
                        ${linkHtml}
                    </div>
                    <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in flex-shrink-0">
                        <input type="checkbox" id="toggle-${serviceName}" ${isChecked} 
                               onchange="toggleService('${serviceName}')"
                               class="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-4 border-gray-600 appearance-none cursor-pointer transition-transform duration-300 ease-in-out z-10 top-0 left-0 checked:translate-x-full checked:border-blue-500"/>
                        <label for="toggle-${serviceName}" class="toggle-label block overflow-hidden h-5 rounded-full bg-gray-600 cursor-pointer transition-colors duration-300 ease-in-out"></label>
                    </div>
                </div>
            `;
            container.innerHTML += html;
        }
    } catch (error) {
        console.error("Lỗi lấy danh sách dịch vụ:", error);
    }
}

// Bật/Tắt Service khi gạt công tắc
async function toggleService(serviceName) {
    try {
        await fetchWithAuth(`${API_BASE_URL}/dashboard/services/toggle/${serviceName}`, {
            method: 'POST'
        });
        
        // Đợi 500ms để server kịp xử lý (đặc biệt là Cloudflare sinh link) rồi mới render lại
        setTimeout(fetchServices, 500); 
    } catch (error) {
        console.error("Lỗi thay đổi trạng thái dịch vụ:", error);
        fetchServices(); // Nếu lỗi thì load lại danh sách để reset trạng thái nút gạt
    }
}

// ==========================================
// 4. KHỞI CHẠY HỆ THỐNG
// ==========================================
document.addEventListener('DOMContentLoaded', checkAuth);