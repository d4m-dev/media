<?php
include '../inc/db.php';
session_start();

// Kiểm tra nếu người dùng đã gửi form yêu cầu reset mật khẩu
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $email = $_POST['email'];

    // Kiểm tra nếu email tồn tại trong cơ sở dữ liệu
    $stmt = $conn->prepare("SELECT * FROM users WHERE email = :email");
    $stmt->bindParam(':email', $email);
    $stmt->execute();
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user) {
        // Tạo mã OTP
        $otp_code = rand(100000, 999999);  // Mã OTP 6 chữ số

        // Lưu OTP vào bảng password_reset
        $stmt = $conn->prepare("INSERT INTO password_reset (user_id, otp_code) VALUES (:user_id, :otp_code)");
        $stmt->bindParam(':user_id', $user['id']);
        $stmt->bindParam(':otp_code', $otp_code);
        $stmt->execute();

        // Gửi OTP qua email (sử dụng PHPMailer hoặc mail() trong PHP)
        $to = $email;
        $subject = "Mã OTP để reset mật khẩu";
        $message = "Mã OTP của bạn để reset mật khẩu là: $otp_code\n\nVui lòng nhập mã OTP trong vòng 15 phút.";
        $headers = "From: no-reply@yourwebsite.com";

        // Gửi email (bạn cần cấu hình máy chủ email hoặc sử dụng PHPMailer)
        if (mail($to, $subject, $message, $headers)) {
            $_SESSION['email'] = $email;  // Lưu email vào session để chuyển qua trang nhập OTP
            header("Location: reset_password.php");  // Chuyển hướng đến trang reset_password.php
        } else {
            $error_message = "Gửi email thất bại. Vui lòng thử lại!";
        }
    } else {
        $error_message = "Email không tồn tại trong hệ thống!";
    }
}
?>

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quên mật khẩu</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white flex flex-col min-h-screen">
<?php include('../templates/header.php'); ?>
 <main class="flex-grow flex items-center justify-center">
    <div class="w-full max-w-md p-8 bg-white shadow-lg rounded-lg">
        <h2 class="text-2xl font-semibold text-center mb-6">Quên mật khẩu</h2>
        <?php if (isset($error_message)): ?>
            <div class="text-red-500 text-center mb-4"><?php echo $error_message; ?></div>
        <?php endif; ?>
        <form action="" method="POST" class="space-y-6">
            <input type="email" name="email" placeholder="Nhập email của bạn" class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-300" required>
            <button type="submit" class="w-full bg-green-500 text-white py-3 rounded-md hover:bg-green-400 focus:ring-2 focus:ring-green-300">Gửi OTP</button>
        </form>
        <div class="mt-4 text-center">
            <p class="text-gray-600">Quay lại <a href="../login.php" class="text-green-500 hover:underline">Đăng nhập</a></p>
        </div>
    </div>
</main>
<?php include('../templates/footer.php'); ?>
</body>
</html>