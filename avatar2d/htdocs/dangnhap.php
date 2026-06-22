<?php
header('Content-Type: application/json; charset=utf-8');
require_once 'inc/db.php';

// Kiểm tra method
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['status' => 'error', 'message' => 'Phương thức không hợp lệ']);
    exit;
}

// Nhận dữ liệu từ POST
$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';

if (empty($username) || empty($password)) {
    echo json_encode(['status' => 'error', 'message' => 'Vui lòng nhập đầy đủ tài khoản và mật khẩu']);
    exit;
}

// Chuẩn bị truy vấn SQL an toàn (Prepared Statement)
$stmt = $conn->prepare("SELECT id, name, avatar, level FROM users WHERE name = ? AND password = ?");
if ($stmt === false) {
    echo json_encode(['status' => 'error', 'message' => 'Lỗi hệ thống']);
    exit;
}

// Mã hóa mật khẩu (giả sử dùng MD5 như trong DB hiện tại)
$hashed = md5($password);
$stmt->bind_param('ss', $username, $hashed);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows === 1) {
    $user = $result->fetch_assoc();
    echo json_encode([
        'status' => 'success',
        'message' => 'Đăng nhập thành công!',
        'user' => $user
    ], JSON_UNESCAPED_UNICODE);
} else {
    echo json_encode([
        'status' => 'error',
        'message' => 'Sai tài khoản hoặc mật khẩu!'
    ], JSON_UNESCAPED_UNICODE);
}

$stmt->close();
$conn->close();
?>