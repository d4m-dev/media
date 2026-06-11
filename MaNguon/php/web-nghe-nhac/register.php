<?php
include 'inc/db.php';
session_start();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $email = $_POST['email'];
    $password = $_POST['password'];
    $confirm_password = $_POST['confirm_password'];
    
    // Kiểm tra email hợp lệ
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $error_message = "Email không hợp lệ!";
    } elseif ($password != $confirm_password) {
        $error_message = "Mật khẩu xác nhận không khớp!";
    } elseif (strlen($password) < 6) {
        $error_message = "Mật khẩu phải có ít nhất 6 ký tự!";
    } else {
        $password_hash = password_hash($password, PASSWORD_DEFAULT);

        // Kiểm tra nếu email hoặc username đã tồn tại
        $stmt = $conn->prepare("SELECT * FROM users WHERE email = :email OR username = :username");
        $stmt->bindParam(':email', $email);
        $stmt->bindParam(':username', $username);
        $stmt->execute();
        
        if ($stmt->rowCount() > 0) {
            $error_message = "Tài khoản đã tồn tại!";
        } else {
            // Thêm người dùng mới vào cơ sở dữ liệu
            $stmt = $conn->prepare("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)");
            $stmt->bindParam(':username', $username);
            $stmt->bindParam(':email', $email);
            $stmt->bindParam(':password', $password_hash);
            $stmt->execute();

            // Sau khi đăng ký thành công, chuyển hướng tới trang register_success.php
            $_SESSION['username'] = $username;
            $_SESSION['email'] = $email;
            header("Location: private/register_success.php"); // Chuyển hướng
            exit(); // Đảm bảo kết thúc script ngay sau khi chuyển hướng
        }
    }
}
?>

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Đăng ký</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white flex flex-col min-h-screen">
<?php include('templates/header.php'); ?>
 <main class="flex-grow flex items-center justify-center">
    <div class="w-full max-w-md p-8 bg-white shadow-lg rounded-lg">
        <h2 class="text-2xl font-semibold text-center mb-6">Đăng ký</h2>
        <?php if (isset($error_message)): ?>
            <div class="text-red-500 text-center mb-4"><?php echo $error_message; ?></div>
        <?php endif; ?>
        <form action="" method="POST" class="space-y-6">
            <input type="text" name="username" placeholder="Tên tài khoản" class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-300" required>
            <input type="email" name="email" placeholder="Email" class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-300" required>
            <input type="password" name="password" placeholder="Mật khẩu" class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-300" required>
            <input type="password" name="confirm_password" placeholder="Xác nhận mật khẩu" class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-300" required>
            
            <button type="submit" class="w-full bg-green-500 text-white py-3 rounded-md hover:bg-green-400 focus:ring-2 focus:ring-green-300">Đăng ký</button>
        </form>
        <div class="mt-4 text-center">
            <p class="text-gray-600">Đã có tài khoản? <a href="login.php" class="text-green-500 hover:underline">Đăng nhập ngay</a></p>
        </div>
    </div>
</main>
<?php include('templates/menu.php'); ?>
<?php include('templates/footer.php'); ?>
</body>
</html>