<?php
include 'inc/db.php';
session_start();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $email_or_username = $_POST['email_or_username'];
    $password = $_POST['password'];
    $remember_me = isset($_POST['remember_me']) ? true : false;

    // Kiểm tra email hoặc tên tài khoản
    $stmt = $conn->prepare("SELECT * FROM users WHERE username = :email_or_username OR email = :email_or_username");
    $stmt->bindParam(':email_or_username', $email_or_username);
    $stmt->execute();
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user && password_verify($password, $user['password'])) {
        $_SESSION['user'] = $user;

        if ($remember_me) {
            setcookie("user", serialize($user), time() + 2 * 24 * 60 * 60, "/");
        }
        
        header("Location: index.php"); // Chuyển hướng tới trang chủ sau khi đăng nhập thành công
    } else {
        $error_message = "Sai tài khoản hoặc mật khẩu!";
    }
}
?>

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Đăng nhập</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>

<body class="bg-white min-h-screen flex flex-col">
<?php include('templates/header.php'); ?>
 <main class="flex-grow flex items-center justify-center">
    <div class="w-full max-w-md p-8 bg-white shadow-lg rounded-lg">
        <h2 class="text-2xl font-semibold text-center mb-6">Đăng nhập</h2>
        <?php if (isset($error_message)): ?>
            <div class="text-red-500 text-center mb-4"><?php echo $error_message; ?></div>
        <?php endif; ?>
        <form action="" method="POST" class="space-y-6">
            <input type="text" name="email_or_username" placeholder="Email hoặc Tên tài khoản" class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-300" required>
            <input type="password" name="password" placeholder="Mật khẩu" class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-300" required>
            
            <div class="flex items-center">
                <input type="checkbox" name="remember_me" class="mr-2"> Ghi nhớ tôi
            </div>
            
            <button type="submit" class="w-full bg-green-500 text-white py-3 rounded-md hover:bg-green-400 focus:ring-2 focus:ring-green-300">Đăng nhập</button>
        </form>
        <div class="mt-4 text-center">
            <a href="private/forgot_password.php" class="text-green-500 hover:underline">Quên mật khẩu?</a>
        </div>
        <div class="mt-4 text-center">
            <p class="text-gray-600">Chưa có tài khoản? <a href="register.php" class="text-green-500 hover:underline">Đăng ký ngay</a></p>
        </div>
    </div>
</main>
<?php include('templates/menu.php'); ?>
<?php include('templates/footer.php'); ?>
</body>
</html>