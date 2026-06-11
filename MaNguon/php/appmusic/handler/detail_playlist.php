<?php
include '../inc/db.php';
session_start();

if (!isset($_SESSION['user'])) {
  header('Location: ../login.php');
  exit;
}

$user_id = $_SESSION['user']['id'];
$playlist_id = $_GET['id'] ?? null;

if (!$playlist_id) {
  header('Location: ../index.php');
  exit;
}

// Lấy thông tin playlist
$stmt = $conn->prepare("SELECT * FROM playlists WHERE id = ? AND user_id = ?");
$stmt->execute([$playlist_id, $user_id]);
$playlist = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$playlist) {
  header('Location: ../index.php');
  exit;
}

// Lấy các bài hát trong playlist
$stmt2 = $conn->prepare("SELECT s.* FROM songs s
                         JOIN playlist_items pi ON s.id = pi.song_id
                         WHERE pi.playlist_id = ?");
$stmt2->execute([$playlist_id]);
$songs = $stmt2->fetchAll(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Playlist Chi Tiết - <?= htmlspecialchars($playlist['name']) ?></title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.0/font/bootstrap-icons.css" rel="stylesheet">
  <style>
    .search-container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      margin-top: 20px;
    }
    .search-input {
      border-radius: 12px; /* Bo góc ô input */
      padding: 10px 20px;
      width: 100%;
      max-width: 400px;
      border: 1px solid #38a169; /* Viền màu xanh lá */
      outline: none;
    }
    .search-input::placeholder {
      color: #38a169; /* Màu chữ placeholder */
    }
    .search-button {
      background-color: #38a169; /* Màu nền nút xanh lá */
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 12px;
      margin-left: 10px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
    .search-button:hover {
      background-color: #48bb78; /* Màu xanh lá nhạt khi hover */
    }
  </style>
</head>
<body class="bg-white font-sans">

<?php include('../templates/header.php'); ?>

<div class="container mx-auto max-w-[90%] mt-[20px] pb-[40px]">
  <h2 class="text-black text-center text-2xl font-bold mb-10">🎧 Playlist: <?= htmlspecialchars($playlist['name']) ?></h2>

  <?php if (empty($songs)): ?>
    <p class="text-white text-center">Playlist này chưa có bài hát nào.</p>
  <?php else: ?>
    <div class="space-y-5">
      <?php foreach ($songs as $song): ?>
        <div class="bg-white rounded-xl p-5 shadow-md hover:scale-[1.01] transition-transform">
          <a href="../pages/player.php?id=<?= $song['id']; ?>" class="flex items-center w-full">
            <div class="flex-shrink-0">
              <img src="<?= htmlspecialchars($song['cover_path']) ?>" alt="Song Image" class="h-[80px] w-[80px] object-cover rounded-lg">
            </div>
            <div class="ml-4">
              <strong class="font-medium"><?= htmlspecialchars($song['title']) ?></strong>
              <p class="mt-1 text-gray-500"><?= htmlspecialchars($song['artist']) ?> • <?= htmlspecialchars($song['genre']) ?></p>
            </div>
          </a>
        </div>
      <?php endforeach; ?>
    </div>
  <?php endif; ?>

</div>

<?php include('../templates/menu.php'); ?>
<?php include('../templates/footer.php'); ?>
</body>
</html>