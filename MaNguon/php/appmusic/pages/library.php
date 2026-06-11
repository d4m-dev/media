<?php
include '../inc/db.php';
session_start();

// Kiểm tra nếu người dùng đã đăng nhập
if (!isset($_SESSION['user'])) {
    header("Location: ../login.php");
    exit;
}

$user_id = $_SESSION['user']['id'];

// Lấy thống kê mỗi thể loại
$stmt = $conn->query("
    SELECT genre,
           COUNT(*) AS song_count,
           SUM(views) AS total_views,
           GROUP_CONCAT(DISTINCT artist ORDER BY artist SEPARATOR '||') AS artists,
           MAX(cover_path) AS any_cover
    FROM songs
    WHERE genre IS NOT NULL AND genre <> ''
    GROUP BY genre
    ORDER BY song_count DESC
");

$genres = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Truy vấn danh sách bài hát yêu thích
$favorites_query = "SELECT COUNT(*) AS total_favorites
                    FROM favorites
                    JOIN songs ON favorites.song_id = songs.id
                    WHERE favorites.user_id = :user_id";
$stmt = $conn->prepare($favorites_query);
$stmt->bindParam(':user_id', $user_id);
$stmt->execute();
$favorites_count = $stmt->fetch(PDO::FETCH_ASSOC)['total_favorites'];

// Truy vấn lịch sử nghe nhạc
$history_query = "SELECT COUNT(*) AS total_history
                  FROM listening_history
                  JOIN songs ON listening_history.song_id = songs.id
                  WHERE listening_history.user_id = :user_id";
$stmt = $conn->prepare($history_query);
$stmt->bindParam(':user_id', $user_id);
$stmt->execute();
$history_count = $stmt->fetch(PDO::FETCH_ASSOC)['total_history'];

// Truy vấn tổng số danh sách phát
$playlist_query = "SELECT COUNT(*) AS total_playlists FROM playlists WHERE user_id = :user_id";
$stmt = $conn->prepare($playlist_query);
$stmt->bindParam(':user_id', $user_id);
$stmt->execute();
$playlist_count = $stmt->fetch(PDO::FETCH_ASSOC)['total_playlists'];
?>

<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Thư Viện</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    .card:hover {
      transform: scale(1.05);
    }

    /* CSS cho hình ảnh bên trong card */
    .card {
      position: relative; /* Để cho phép hình ảnh tuyệt đối bên trong */
    }

    .card-image {
      height: 100%;
      width: 25%;
      object-fit: cover; /* Đảm bảo ảnh không bị méo */
      position: absolute;
      left: 0;
      top: 0;
      border-top-left-radius: 8px;  /* Bo góc trên bên trái */
      border-bottom-left-radius: 8px; /* Bo góc dưới bên trái */
    }

    .card-content {
      padding-left: 27%; /* Đẩy nội dung sang phải để không bị che mất */
      padding-top: 4px; /* Khoảng cách giữa nội dung và ảnh */
    }
  </style>
</head>
<body class="bg-gray-100">

<?php include('../templates/header.php'); ?>

<!-- Main Content -->
<div class="container mx-auto p-4">
  <div class="space-y-8">
    
    <!-- Playlist Section -->
    <section>
      <h2 class="text-2xl font-bold text-green-500">Danh sách phát của tôi</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div class="card p-4 border rounded-lg bg-white shadow-md cursor-pointer" onclick="window.location.href='../pages/playlist.php'">
          <img src="https://i.postimg.cc/pV5YXTfH/my-playlist.jpg" alt="Playlist Image" class="card-image">
          <div class="card-content">
            <i class="bi bi-heart-fill text-red-500 text-4xl"></i>
            <h3 class="font-semibold text-lg mt-4">Danh sách phát</h3>
            <p class="text-gray-500"><?= $playlist_count ?> danh sách</p>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Favorites Section -->
    <section>
      <h2 class="text-2xl font-bold text-green-500">Bài Hát Yêu Thích</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div class="card p-4 border rounded-lg bg-white shadow-md cursor-pointer" onclick="window.location.href='../handler/detail_favorite.php'">
          <img src="https://i.postimg.cc/NFKfcFLC/my-favorite.png" alt="Favorite Song Image" class="card-image">
          <div class="card-content">
            <i class="bi bi-heart-fill text-red-500 text-4xl"></i>
            <h3 class="font-semibold text-lg mt-4">Bài hát yêu thích</h3>
            <p class="text-gray-500"><?= $favorites_count ?> bài hát</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Listening History Section -->
    <section>
      <h2 class="text-2xl font-bold text-green-500">Lịch Sử Nghe Nhạc</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div class="card p-4 border rounded-lg bg-white shadow-md cursor-pointer" onclick="window.location.href='../handler/detail_history.php'">
          <img src="https://i.postimg.cc/pdFysP6f/history.png" alt="History Song Image" class="card-image">
          <div class="card-content">
            <i class="bi bi-clock-history text-blue-500 text-4xl"></i>
            <h3 class="font-semibold text-lg mt-4">Lịch sử nghe</h3>
            <p class="text-gray-500"><?= $history_count ?> bài hát</p>
          </div>
        </div>
      </div>
    </section>

  </div>
</div>

<?php include('../templates/menu.php'); ?>
<?php include('../templates/footer.php'); ?>

</body>
</html>