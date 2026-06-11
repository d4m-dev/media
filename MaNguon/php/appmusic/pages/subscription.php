<?php
include '../inc/db.php';
session_start();

// Kiểm tra người dùng đã đăng nhập chưa
if (!isset($_SESSION['user'])) {
    header('Location: ../login.php');
    exit;
}

$user_id = $_SESSION['user']['id'];

// Lấy thông tin đăng ký của người dùng
$stmt = $conn->prepare("SELECT us.*, sp.plan_name, sp.price, sp.duration, sp.description FROM user_subscriptions us
                        JOIN subscription_plans sp ON us.plan_id = sp.id
                        WHERE us.user_id = ?");
$stmt->execute([$user_id]);
$subscription = $stmt->fetch(PDO::FETCH_ASSOC);

// Nếu người dùng chưa có đăng ký
if (!$subscription) {
    $subscription = [
        'plan_name' => 'free',
        'price' => 0.00,
        'duration' => 30,
        'description' => 'Gói miễn phí dành cho người dùng.',
        'start_date' => date('Y-m-d'),
        'end_date' => '9999-12-31',  // Đặt ngày hết hạn là vĩnh viễn cho gói Free
        'status' => 'active'
    ];
}

?>

<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Trạng thái Đăng Ký</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    .card {
        max-width: 380px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
  </style>
</head>
<body class="bg-gray-100 font-sans">

<?php include('../templates/header.php'); ?>

<div class="mb-8 container mx-auto max-w-screen-md p-6 mt-8 bg-white rounded-lg shadow-lg">
  <h2 class="text-2xl font-semibold text-center mb-6">Trạng Thái Đăng Ký Của Bạn</h2>

  <!-- Hiển thị thông tin người dùng -->
  <div class="mb-6">
    <p class="text-lg">Tên người dùng: <strong><?= htmlspecialchars($_SESSION['user']['username']) ?></strong></p>
    <p class="text-lg">Gói đăng ký hiện tại: <strong><?= htmlspecialchars($subscription['plan_name']) ?></strong></p>
    <p class="text-lg">Thời gian còn lại: 
        <strong>
          <?php
            // Nếu gói Free, hiển thị thời gian vĩnh viễn
            if ($subscription['plan_name'] == 'free') {
                echo 'Vĩnh viễn';
            } else {
                echo $subscription['status'] == 'active' ? 
                (new DateTime($subscription['end_date']))->diff(new DateTime())->format('%a ngày') : 
                'Đã hết hạn';
            }
          ?>
        </strong>
    </p>
  </div>

  <!-- Hiển thị 2 gói đăng ký -->
  <div class="space-y-4">
    <!-- Gói Free -->
    <div class="card p-6 bg-green-100 rounded-lg">
      <h3 class="text-xl font-semibold mb-3">Gói Free</h3>
      <p class="text-lg mb-3">Miễn phí</p>
      <p class="text-sm mb-3"><?= $subscription['plan_name'] == 'free' ? 'Đang sử dụng' : 'Bạn chưa đăng ký' ?></p>
      <p class="text-sm"><?= $subscription['plan_name'] == 'free' ? 'Tận hưởng gói miễn phí với quyền truy cập cơ bản.' : '' ?></p>
      <p class="text-sm">Miễn phí, không yêu cầu thanh toán.</p>
    </div>

    <!-- Gói Premium -->
    <div class="card p-6 bg-yellow-100 rounded-lg">
      <h3 class="text-xl font-semibold mb-3">Gói Premium</h3>
      <p class="text-lg mb-3">$0.99 USD</p>
      <p class="text-sm mb-3"><?= $subscription['plan_name'] == 'premium' ? 'Đang sử dụng' : 'Bạn chưa đăng ký' ?></p>
      <p class="text-sm"><?= $subscription['plan_name'] == 'premium' ? 'Tận hưởng mọi tính năng cao cấp với gói Premium.' : '' ?></p>
      <p class="text-sm">Giá trị: 30 ngày sử dụng.</p>
      <?php if ($subscription['plan_name'] != 'premium'): ?>
        <a href="../handler/process_subscription.php?plan=premium" class="mt-3 inline-block bg-yellow-600 text-white px-4 py-2 rounded-md hover:bg-yellow-700">Chọn Gói Premium</a>
      <?php endif; ?>
    </div>
  </div>

</div>

<script>
  // Handle actions if needed (like subscription change or cancellation)
</script>

<?php include('../templates/footer.php'); ?>
<?php include('../templates/menu.php'); ?>

</body>
</html>