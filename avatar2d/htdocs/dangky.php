<?php
header('Content-Type: application/json; charset=utf-8');
require_once 'inc/db.php';

// Nhận dữ liệu từ POST
$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';
$response = [];

// Kiểm tra hợp lệ
if (!$username || !$password || strlen($username) < 4 || strlen($password) < 4) {
    echo json_encode(['status' => 'error', 'message' => 'Tên & mật khẩu phải từ 4 ký tự trở lên']);
    exit;
}

// Kiểm tra tên đã tồn tại chưa
$stmt_check = $conn->prepare("SELECT id FROM users WHERE name = ?");
$stmt_check->bind_param('s', $username);
$stmt_check->execute();
$stmt_check->store_result();

if ($stmt_check->num_rows > 0) {
    echo json_encode(['status' => 'error', 'message' => 'Tên tài khoản đã tồn tại']);
    $stmt_check->close();
    exit;
}
$stmt_check->close();

// Mã hóa mật khẩu (dùng MD5 giống bảng `users`)
$password_hashed = md5($password);

// Tạo tài khoản mới
$stmt_insert = $conn->prepare("
    INSERT INTO users (name, password, datereg, level, hp, hpfull, sucmanh, xu)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
");

if (!$stmt_insert) {
    echo json_encode(['status' => 'error', 'message' => 'Lỗi chuẩn bị truy vấn']);
    exit;
}

$now = time();
$level = 1;
$hp = 100;
$hpfull = 100;
$sucmanh = 10;
$xu = 500;

$stmt_insert->bind_param('ssiiiiii', $username, $password_hashed, $now, $level, $hp, $hpfull, $sucmanh, $xu);
$success = $stmt_insert->execute();

if ($success) {
    echo json_encode(['status' => 'success', 'message' => '🟢 Đăng ký thành công!']);
} else {
    echo json_encode(['status' => 'error', 'message' => '❌ Lỗi khi đăng ký người chơi']);
}

$stmt_insert->close();
$conn->close();
?>