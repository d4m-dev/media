<?php
include '../inc/db.php';
session_start();

// Kiểm tra người dùng đã đăng nhập chưa
if (!isset($_SESSION['user'])) {
    header('Location: ../login.php');
    exit;
}

$user_id = $_SESSION['user']['id'];
$plan = $_GET['plan'] ?? '';

// Kiểm tra nếu người dùng đã chọn một gói hợp lệ
if ($plan != 'free' && $plan != 'premium') {
    $_SESSION['error'] = 'Gói đăng ký không hợp lệ.';
    header('Location: ../pages/subscription.php');
    exit;
}

// Lấy ID của gói đã chọn
$stmt = $conn->prepare("SELECT id FROM subscription_plans WHERE plan_name = ?");
$stmt->execute([$plan]);
$plan_data = $stmt->fetch(PDO::FETCH_ASSOC);

// Nếu không tìm thấy gói
if (!$plan_data) {
    $_SESSION['error'] = 'Không tìm thấy gói đăng ký này.';
    header('Location: ../pages/subscription.php');
    exit;
}

// Cập nhật thông tin đăng ký cho người dùng
$plan_id = $plan_data['id'];
$start_date = date('Y-m-d');
$end_date = date('Y-m-d', strtotime('+30 days')); // Thời gian thuê bao là 30 ngày

// Kiểm tra nếu người dùng đã đăng ký gói này rồi
$stmt_check = $conn->prepare("SELECT * FROM user_subscriptions WHERE user_id = ?");
$stmt_check->execute([$user_id]);
$existing_subscription = $stmt_check->fetch(PDO::FETCH_ASSOC);

if ($existing_subscription) {
    $_SESSION['error'] = 'Bạn đã có một đăng ký. Hãy hủy đăng ký cũ trước khi đăng ký mới.';
    header('Location: ../pages/subscription.php');
    exit;
}

// Thêm đăng ký mới vào bảng user_subscriptions
$stmt_insert = $conn->prepare("INSERT INTO user_subscriptions (user_id, plan_id, start_date, end_date, status) 
                               VALUES (?, ?, ?, ?, 'active')");
$stmt_insert->execute([$user_id, $plan_id, $start_date, $end_date]);

// Thông báo thành công và chuyển hướng đến trang thanh toán (hoặc trang xác nhận)
$_SESSION['success'] = 'Đăng ký thành công! Bạn sẽ được chuyển đến trang thanh toán để hoàn tất quá trình.';
header('Location: ../private/payment.php');
exit;
