<?php
include '../inc/db.php';
session_start();

// Kiểm tra người dùng đã đăng nhập chưa
if (!isset($_SESSION['user'])) {
    header('Location: ../login.php');
    exit;
}

// Kiểm tra trạng thái đăng ký từ session
$status_message = '';
$status_color = '';

// Nếu có thông báo thành công
if (isset($_SESSION['success'])) {
    $status_message = $_SESSION['success'];
    $status_color = 'bg-green-500 text-white';  // Màu xanh lá cho thành công
    unset($_SESSION['success']);
}

// Nếu có thông báo lỗi
if (isset($_SESSION['error'])) {
    $status_message = $_SESSION['error'];
    $status_color = 'bg-red-500 text-white';  // Màu đỏ cho lỗi
    unset($_SESSION['error']);
}

?>

<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Thanh Toán</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans">

<?php include('../templates/header.php'); ?>

<div class="container mx-auto max-w-lg p-6 mt-8 bg-white rounded-lg shadow-lg">
  <h2 class="text-2xl font-semibold text-center mb-6">Trang Thanh Toán</h2>

  <!-- Hiển thị thông báo trạng thái đăng ký -->
  <?php if ($status_message): ?>
    <div class="p-4 mb-6 rounded-md <?= $status_color ?> text-center">
      <p><?= $status_message ?></p>
    </div>
  <?php endif; ?>

  <!-- Hiển thị nút đăng ký thanh toán (hiện tại là thử nghiệm) -->
  <div class="text-center">
    <a href="payment_success.php" class="bg-blue-500 text-white px-6 py-3 rounded-md hover:bg-blue-600 transition">Hoàn tất Đăng Ký</a>
  </div>
</div>

<?php include('../templates/footer.php'); ?>
<?php include('../templates/menu.php'); ?>

</body>
</html>