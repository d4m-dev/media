const toggleBtn = document.getElementById('toggleMode');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const messageBox = document.getElementById('message');

let mode = 'login';

// 👉 Chuyển đổi giữa đăng nhập và đăng ký
toggleBtn.addEventListener('click', () => {
  if (mode === 'login') {
    loginForm.style.display = 'none';
    registerForm.style.display = 'flex';
    toggleBtn.textContent = '← Quay lại đăng nhập';
    mode = 'register';
  } else {
    loginForm.style.display = 'flex';
    registerForm.style.display = 'none';
    toggleBtn.textContent = '→ Nếu chưa có tài khoản, đăng ký';
    mode = 'login';
  }
  messageBox.textContent = '';
});

// 🟢 Xử lý đăng nhập
loginForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();

  if (!username || !password) {
    messageBox.textContent = '⚠️ Vui lòng nhập đầy đủ tài khoản và mật khẩu!';
    return;
  }

  fetch('https://d4m-dev.kesug.com/dangnhap.php', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === 'success') {
      messageBox.innerHTML = `🟢 Xin chào <b>${data.user.name}</b>! Level: ${data.user.level}`;
      // Có thể lưu sessionStorage và chuyển sang màn chơi
    } else {
      messageBox.textContent = `🔴 ${data.message}`;
    }
  })
  .catch(() => {
    messageBox.textContent = '❌ Lỗi kết nối đến máy chủ!';
  });
});

// 🟡 Xử lý đăng ký
registerForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const username = document.getElementById('newUsername').value.trim();
  const password = document.getElementById('newPassword').value.trim();

  if (!username || !password) {
    messageBox.textContent = '⚠️ Vui lòng nhập đầy đủ thông tin!';
    return;
  }

  fetch('https://d4m-dev.kesug.com/dangky.php', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === 'success') {
      messageBox.textContent = '🟢 Đăng ký thành công! Bạn có thể đăng nhập.';
      registerForm.reset();
    } else {
      messageBox.textContent = `🔴 ${data.message}`;
    }
  })
  .catch(() => {
    messageBox.textContent = '❌ Lỗi kết nối đến máy chủ!';
  });
});