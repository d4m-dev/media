// Authentication UI for Music Pro
class AuthUI {
    constructor(app) {
        this.app = app;
        this.init();
    }

    init() {
        this.createAuthModals();
        this.updateAuthUI();
    }

    createAuthModals() {
        // Create Login Modal
        let loginModal = document.getElementById('login-modal');
        if (!loginModal) {
            loginModal = document.createElement('div');
            loginModal.id = 'login-modal';
            loginModal.className = 'modal-overlay';
            loginModal.innerHTML = `
                <div class="modal-content" style="max-width: 400px; width: 90%; max-height: 85vh; overflow-y: auto; border-radius: 16px; padding: 24px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                        <h3 style="margin: 0; font-size: 20px; font-weight: 700;">Đăng nhập</h3>
                        <button class="btn-close-modal" style="width: 32px; height: 32px; border-radius: 50%; background: var(--bg-secondary); border: none; color: var(--text-main); display: flex; align-items: center; justify-content: center; cursor: pointer;"><i class="fa-solid fa-xmark"></i></button>
                    </div>
                    <div style="margin-bottom: 20px;">
                        <div style="margin-bottom: 15px;">
                            <label for="login-email" style="display: block; margin-bottom: 8px; color: var(--text-main);">Email:</label>
                            <input type="email" id="login-email" placeholder="Nhập email của bạn" style="width: 100%; padding: 12px; border-radius: 8px; background: var(--bg-secondary); color: var(--text-main); border: 1px solid var(--border); font-size: 16px;">
                        </div>
                        <div style="margin-bottom: 20px;">
                            <label for="login-password" style="display: block; margin-bottom: 8px; color: var(--text-main);">Mật khẩu:</label>
                            <input type="password" id="login-password" placeholder="Nhập mật khẩu" style="width: 100%; padding: 12px; border-radius: 8px; background: var(--bg-secondary); color: var(--text-main); border: 1px solid var(--border); font-size: 16px;">
                        </div>
                        <button id="btn-login-submit" style="width: 100%; background: var(--primary); color: white; padding: 12px; border-radius: 12px; font-weight: 600; margin-bottom: 15px;">Đăng nhập</button>
                        <div style="text-align: center; font-size: 14px; color: var(--text-sub);">Chưa có tài khoản? <a href="#" id="switch-to-signup" style="color: var(--primary); cursor: pointer;">Đăng ký</a></div>
                    </div>
                </div>
            `;
            document.body.appendChild(loginModal);
        }

        // Create Signup Modal
        let signupModal = document.getElementById('signup-modal');
        if (!signupModal) {
            signupModal = document.createElement('div');
            signupModal.id = 'signup-modal';
            signupModal.className = 'modal-overlay';
            signupModal.innerHTML = `
                <div class="modal-content" style="max-width: 400px; width: 90%; max-height: 85vh; overflow-y: auto; border-radius: 16px; padding: 24px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                        <h3 style="margin: 0; font-size: 20px; font-weight: 700;">Đăng ký</h3>
                        <button class="btn-close-modal" style="width: 32px; height: 32px; border-radius: 50%; background: var(--bg-secondary); border: none; color: var(--text-main); display: flex; align-items: center; justify-content: center; cursor: pointer;"><i class="fa-solid fa-xmark"></i></button>
                    </div>
                    <div style="margin-bottom: 20px;">
                        <div style="margin-bottom: 15px;">
                            <label for="signup-email" style="display: block; margin-bottom: 8px; color: var(--text-main);">Email:</label>
                            <input type="email" id="signup-email" placeholder="Nhập email của bạn" style="width: 100%; padding: 12px; border-radius: 8px; background: var(--bg-secondary); color: var(--text-main); border: 1px solid var(--border); font-size: 16px;">
                        </div>
                        <div style="margin-bottom: 15px;">
                            <label for="signup-password" style="display: block; margin-bottom: 8px; color: var(--text-main);">Mật khẩu:</label>
                            <input type="password" id="signup-password" placeholder="Nhập mật khẩu" style="width: 100%; padding: 12px; border-radius: 8px; background: var(--bg-secondary); color: var(--text-main); border: 1px solid var(--border); font-size: 16px;">
                        </div>
                        <div style="margin-bottom: 20px;">
                            <label for="signup-confirm-password" style="display: block; margin-bottom: 8px; color: var(--text-main);">Xác nhận mật khẩu:</label>
                            <input type="password" id="signup-confirm-password" placeholder="Xác nhận mật khẩu" style="width: 100%; padding: 12px; border-radius: 8px; background: var(--bg-secondary); color: var(--text-main); border: 1px solid var(--border); font-size: 16px;">
                        </div>
                        <button id="btn-signup-submit" style="width: 100%; background: var(--primary); color: white; padding: 12px; border-radius: 12px; font-weight: 600; margin-bottom: 15px;">Đăng ký</button>
                        <div style="text-align: center; font-size: 14px; color: var(--text-sub);">Đã có tài khoản? <a href="#" id="switch-to-login" style="color: var(--primary); cursor: pointer;">Đăng nhập</a></div>
                    </div>
                </div>
            `;
            document.body.appendChild(signupModal);
        }

        // Add event listeners
        this.addAuthEventListeners();
    }

    addAuthEventListeners() {
        // Login modal events
        const loginModal = document.getElementById('login-modal');
        const signupModal = document.getElementById('signup-modal');
        
        // Close modals
        loginModal.querySelectorAll('.btn-close-modal').forEach(btn => {
            btn.onclick = () => loginModal.classList.remove('show');
        });
        
        signupModal.querySelectorAll('.btn-close-modal').forEach(btn => {
            btn.onclick = () => signupModal.classList.remove('show');
        });
        
        // Switch between login and signup
        document.getElementById('switch-to-signup').onclick = (e) => {
            e.preventDefault();
            loginModal.classList.remove('show');
            signupModal.classList.add('show');
        };
        
        document.getElementById('switch-to-login').onclick = (e) => {
            e.preventDefault();
            signupModal.classList.remove('show');
            loginModal.classList.add('show');
        };
        
        // Login form submission
        document.getElementById('btn-login-submit').onclick = async () => {
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;
            
            if (!email || !password) {
                this.app.showToast('Vui lòng nhập email và mật khẩu');
                return;
            }
            
            const success = await this.app.login(email, password);
            if (success) {
                loginModal.classList.remove('show');
                this.updateAuthUI();
            }
        };
        
        // Signup form submission
        document.getElementById('btn-signup-submit').onclick = async () => {
            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;
            const confirmPassword = document.getElementById('signup-confirm-password').value;
            
            if (!email || !password || !confirmPassword) {
                this.app.showToast('Vui lòng điền đầy đủ thông tin');
                return;
            }
            
            if (password !== confirmPassword) {
                this.app.showToast('Mật khẩu xác nhận không khớp');
                return;
            }
            
            if (password.length < 6) {
                this.app.showToast('Mật khẩu phải có ít nhất 6 ký tự');
                return;
            }
            
            const success = await this.app.signup(email, password);
            if (success) {
                signupModal.classList.remove('show');
                this.updateAuthUI();
            }
        };
        
        // Close modals when clicking outside
        loginModal.onclick = (e) => {
            if (e.target === loginModal) loginModal.classList.remove('show');
        };
        
        signupModal.onclick = (e) => {
            if (e.target === signupModal) signupModal.classList.remove('show');
        };
    }

    updateAuthUI() {
        // Add auth buttons to the settings page if they don't exist
        setTimeout(() => {
            const profileSection = document.querySelector('.settings-section:first-child');
            if (profileSection) {
                // Check if auth buttons already exist
                if (!document.getElementById('auth-buttons-container')) {
                    const authButtons = document.createElement('div');
                    authButtons.id = 'auth-buttons-container';
                    authButtons.style.cssText = `
                        display: flex;
                        gap: 10px;
                        margin-top: 15px;
                        padding-top: 15px;
                        border-top: 1px solid var(--border);
                    `;
                    
                    authButtons.innerHTML = `
                        <button id="btn-show-login" style="flex: 1; background: var(--primary); color: white; padding: 10px; border-radius: 8px; font-weight: 600; border: none; cursor: pointer;">Đăng nhập</button>
                        <button id="btn-logout" style="flex: 1; background: #ff4757; color: white; padding: 10px; border-radius: 8px; font-weight: 600; border: none; cursor: pointer; display: none;">Đăng xuất</button>
                    `;
                    
                    profileSection.appendChild(authButtons);
                    
                    // Add event listeners
                    document.getElementById('btn-show-login').onclick = () => {
                        document.getElementById('login-modal').classList.add('show');
                    };
                    
                    document.getElementById('btn-logout').onclick = async () => {
                        await this.app.logout();
                        this.updateAuthUI();
                    };
                }
                
                // Update button visibility based on auth status
                this.updateAuthButtonVisibility();
            }
        }, 1000); // Delay to ensure settings are rendered
    }

    async updateAuthButtonVisibility() {
        // Check the actual auth status
        let isAnonymous = localStorage.getItem('anonymous_user_id') !== null;
        let isAuthenticated = false;
        
        // Check if there's a Supabase session
        if (window.app && window.app.supabaseIntegration && window.app.supabaseIntegration.supabaseService) {
            try {
                const user = await window.app.supabaseIntegration.supabaseService.getCurrentUser();
                if (user && !user.isAnonymous) {
                    isAuthenticated = true;
                    isAnonymous = false;
                } else if (user && user.isAnonymous) {
                    isAnonymous = true;
                    isAuthenticated = false;
                }
            } catch (error) {
                console.error('Error checking auth status:', error);
            }
        }
        
        const loginBtn = document.getElementById('btn-show-login');
        const logoutBtn = document.getElementById('btn-logout');
        
        if (loginBtn && logoutBtn) {
            if (isAuthenticated) {
                // User is authenticated with Supabase
                loginBtn.style.display = 'none';
                logoutBtn.style.display = 'block';
                
                // Update the profile section to show user info
                const profileItem = document.querySelector('.settings-item'); // First settings item is the profile
                if (profileItem) {
                    const profileName = profileItem.querySelector('.settings-name');
                    const profileDesc = profileItem.querySelector('.settings-desc');
                    
                    if (profileName && profileDesc) {
                        profileName.textContent = 'Tài khoản đã đăng nhập';
                        profileDesc.textContent = 'Đồng bộ dữ liệu với đám mây';
                    }
                }
            } else if (isAnonymous) {
                // User is using anonymous account
                loginBtn.style.display = 'block';
                logoutBtn.style.display = 'block';
                
                // Update the profile section to show anonymous status
                const profileItem = document.querySelector('.settings-item'); // First settings item is the profile
                if (profileItem) {
                    const profileName = profileItem.querySelector('.settings-name');
                    const profileDesc = profileItem.querySelector('.settings-desc');
                    
                    if (profileName && profileDesc) {
                        profileName.textContent = 'Tài khoản ẩn danh';
                        profileDesc.textContent = 'Dữ liệu được lưu cục bộ';
                    }
                }
            } else {
                // User is not logged in at all
                loginBtn.style.display = 'block';
                logoutBtn.style.display = 'none';
                
                // Update the profile section to show not logged in status
                const profileItem = document.querySelector('.settings-item'); // First settings item is the profile
                if (profileItem) {
                    const profileName = profileItem.querySelector('.settings-name');
                    const profileDesc = profileItem.querySelector('.settings-desc');
                    
                    if (profileName && profileDesc) {
                        profileName.textContent = 'Chưa đăng nhập';
                        profileDesc.textContent = 'Đăng nhập để đồng bộ dữ liệu';
                    }
                }
            }
        }
    }
}

// Initialize auth UI when app is ready
document.addEventListener('DOMContentLoaded', () => {
    // Wait for app to be initialized
    const checkApp = setInterval(() => {
        if (window.app) {
            clearInterval(checkApp);
            // Initialize auth UI after a short delay to ensure everything is loaded
            setTimeout(() => {
                if (window.AuthUI) {
                    window.authUI = new AuthUI(window.app);
                }
            }, 1000);
        }
    }, 100);
});