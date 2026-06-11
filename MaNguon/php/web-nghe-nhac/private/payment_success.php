<?php
include '../inc/db.php';
session_start();

// Kiểm tra người dùng đã đăng nhập chưa
if (!isset($_SESSION['user'])) {
    header('Location: ../login.php');
    exit;
}

// Cập nhật trạng thái đăng ký thành công (Chuyển đổi trạng thái nếu cần)
$user_id = $_SESSION['user']['id'];

// Cập nhật trạng thái đăng ký thành "active" trong bảng user_subscriptions
$stmt = $conn->prepare("UPDATE user_subscriptions SET status = 'active' WHERE user_id = ? AND status != 'active'");
$stmt->execute([$user_id]);

?>

<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Đăng Ký Thành Công</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans">

<?php include('../templates/header.php'); ?>

<div class="container mx-auto max-w-lg p-6 mt-8 bg-white rounded-lg shadow-lg mb-[20px]">
  <h2 class="text-2xl font-semibold text-center mb-6">Đăng Ký Thành Công!</h2>
  
  <div class="text-center mb-[30px]">
    <p class="text-lg">Chúc mừng bạn đã đăng ký thành công!</p>
    <p class="mt-4 mb-[10px]">Bây giờ bạn có thể truy cập vào tất cả các tính năng cao cấp.</p>
    <a href="../admin/dashboard.php" class="mt-6 bg-green-500 text-white px-6 py-3 rounded-md hover:bg-green-600 transition mb-[30px]">Đi đến trang Dashboard</a>
  </div>
    <div class="flex justify-center"><a>Hoặc đi đến trang chủ</a>
    </div>
    <div class="flex justify-center"><a href="../index.php" class="mt-6 bg-green-500 text-white px-6 py-3 rounded-md hover:bg-green-600 transition">Trang chủ</a>
    </div>
</div>

<?php include('../templates/footer.php'); ?>
<?php include('../templates/menu.php'); ?>

</body>
</html>