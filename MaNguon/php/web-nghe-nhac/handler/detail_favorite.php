<?php
include '../inc/db.php';
session_start();

// Kiểm tra nếu người dùng đã đăng nhập
if (!isset($_SESSION['user'])) {
    header("Location: ../login.php");
    exit;
}

$user_id = $_SESSION['user']['id'];

// Truy vấn danh sách bài hát yêu thích
$favorites_query = "SELECT songs.id, songs.title, songs.artist, songs.cover_path
                    FROM favorites
                    JOIN songs ON favorites.song_id = songs.id
                    WHERE favorites.user_id = :user_id";
$stmt = $conn->prepare($favorites_query);
$stmt->bindParam(':user_id', $user_id);
$stmt->execute();
$favorites = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bài Hát Yêu Thích</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">

<?php include('../templates/header.php'); ?>

<!-- Main Content -->
<div class="container mx-auto p-4">
  <h2 class="text-2xl font-bold text-green-500 mb-6">Danh Sách Bài Hát Yêu Thích</h2>
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
    <?php foreach ($favorites as $song): ?>
      <div class="card p-4 border rounded-lg bg-white shadow-md">
        <img src="<?= $song['cover_path'] ?>" alt="Cover" class="w-full h-48 object-cover rounded-md mb-4">
        <h3 class="font-semibold text-lg"><?= htmlspecialchars($song['title']) ?></h3>
        <p class="text-gray-500"><?= htmlspecialchars($song['artist']) ?></p>
        <a href="../pages/player.php?id=<?= $song['id'] ?>" class="text-green-500 hover:underline">Nghe ngay</a>
      </div>
    <?php endforeach; ?>
  </div>
</div>

<?php include('../templates/menu.php'); ?>
<?php include('../templates/footer.php'); ?>

</body>
</html>