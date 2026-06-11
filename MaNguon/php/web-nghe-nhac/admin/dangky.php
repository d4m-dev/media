<?php
include 'inc/db.php';  // Kết nối tới cơ sở dữ liệu

// Mã hóa mật khẩu admin
$admin_password = password_hash('admin123', PASSWORD_DEFAULT);

// Thêm tài khoản admin vào cơ sở dữ liệu
$stmt = $conn->prepare("INSERT INTO users (username, password, role) VALUES (:username, :password, :role)");
$stmt->bindParam(':username', $username);
$stmt->bindParam(':password', $admin_password);
$stmt->bindParam(':role', $role);

// Gán giá trị cho tài khoản admin
$username = 'admin';
$role = 'admin'; // Quyền cao nhất

// Thực hiện truy vấn
if ($stmt->execute()) {
    echo "Tạo tài khoản admin thành công!";
} else {
    echo "Lỗi khi tạo tài khoản admin.";
}
?>