<?php
session_start();

// Kiểm tra nếu thông tin tài khoản đã tồn tại trong session
if (!isset($_SESSION['username']) || !isset($_SESSION['email'])) {
    header("Location: ../login.php");
    exit();
}

$username = $_SESSION['username'];
$email = $_SESSION['email'];
?>

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Đăng ký thành công</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white flex flex-col min-h-screen">
<?php include('../templates/header.php'); ?>

<main class="flex-grow flex items-center justify-center">
    <div class="w-full max-w-md p-8 bg-white shadow-lg rounded-lg">
        <h2 class="text-2xl font-semibold text-center mb-6">Đăng ký thành công</h2>
        <div class="text-center">
            <p class="text-green-500">Tài khoản của bạn đã được tạo thành công!</p>
            <p class="text-gray-600 mt-4">Tên tài khoản: <span class="font-semibold"><?php echo $username; ?></span></p>
            <p class="text-gray-600">Email: <span class="font-semibold"><?php echo $email; ?></span></p>

            <div class="mt-4">
                <!-- Nút "Đăng nhập ngay" -->
                <a href="../login.php" class="w-full bg-green-500 text-white py-3 rounded-md hover:bg-green-400 focus:ring-2 focus:ring-green-300 text-center inline-block">Đăng nhập ngay</a>
            </div>

            <!-- Thông báo đếm ngược -->
            <p class="mt-4 text-gray-600">Tự động chuyển về trang đăng nhập sau <span id="countdown">8</span>s</p>
        </div>
    </div>
</main>

<script>
    // Đếm ngược thời gian 8 giây
    let timeLeft = 8;
    const countdownElement = document.getElementById("countdown");

    function updateCountdown() {
        if (timeLeft > 0) {
            timeLeft--;
            countdownElement.textContent = timeLeft;
        } else {
            // Khi thời gian hết, chuyển hướng người dùng đến trang đăng nhập
            window.location.href = "../login.php";
        }
    }

    // Cập nhật mỗi giây
    setInterval(updateCountdown, 1000);

    // Redirect to login page after 8 seconds
    setTimeout(function() {
        window.location.href = "../login.php";
    }, 8000);
</script>

<?php include('../templates/footer.php'); ?>
</body>
</html>