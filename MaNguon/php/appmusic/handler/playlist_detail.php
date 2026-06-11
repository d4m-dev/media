<?php
include '../inc/db.php';
session_start();

if (!isset($_SESSION['user'])) {
  header('Location: login.php');
  exit;
}

$user_id = $_SESSION['user']['id'];
$playlist_id = intval($_GET['id'] ?? 0);

// Kiểm tra playlist thuộc quyền người dùng
$stmt = $conn->prepare("SELECT * FROM playlists WHERE id = ? AND user_id = ?");
$stmt->execute([$playlist_id, $user_id]);
$playlist = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$playlist) {
  http_response_code(403);
  exit('Playlist không tồn tại hoặc bạn không có quyền truy cập.');
}

// Lấy bài hát thuộc playlist
$stmt2 = $conn->prepare("
  SELECT s.*
  FROM songs s
  JOIN playlist_items pi ON s.id = pi.song_id
  WHERE pi.playlist_id = ?
  ORDER BY pi.added_time DESC
");
$stmt2->execute([$playlist_id]);
$songs = $stmt2->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <title><?php echo htmlspecialchars($playlist['name']); ?> | Playlist</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background: linear-gradient(to right, #ffecd2, #fcb69f);
      font-family: 'Segoe UI', sans-serif;
      margin: 0; padding: 0;
    }
    .container {
      max-width: 900px;
      margin: auto;
      padding: 40px 20px;
    }
    h2 {
      text-align: center;
      color: #333;
      margin-bottom: 30px;
    }
    .song-card {
      background: #fff;
      border-radius: 12px;
      padding: 15px;
      display: flex;
      align-items: center;
      box-shadow: 0 4px 16px rgba(0,0,0,0.08);
      margin-bottom: 20px;
      transition: 0.2s ease;
    }
    .song-card:hover {
      transform: scale(1.01);
    }
    .song-card img {
      width: 80px;
      height: 80px;
      object-fit: cover;
      border-radius: 10px;
      margin-right: 20px;
    }
    .info h5 {
      margin: 0 0 5px;
    }
    .info p {
      margin: 0;
      font-size: 14px;
      color: #666;
    }
  </style>
</head>
<body>

<?php include('../templates/banner.php'); ?>

<div class="container">
  <h2>🎧 Playlist: <?php echo htmlspecialchars($playlist['name']); ?></h2>

  <?php if (empty($songs)): ?>
    <p class="text-center text-muted">Playlist này chưa có bài hát nào.</p>
  <?php else: ?>
    <?php foreach ($songs as $song): ?>
      <a href="../pages/player.php?id=<?php echo $song['id']; ?>" class="text-decoration-none text-dark">
        <div class="song-card">
          <img src="<?php echo htmlspecialchars($song['cover_path']); ?>" alt="cover">
          <div class="info">
            <h5><?php echo htmlspecialchars($song['title']); ?></h5>
            <p><?php echo htmlspecialchars($song['artist']); ?> • <?php echo htmlspecialchars($song['genre']); ?></p>
          </div>
        </div>
      </a>
    <?php endforeach; ?>
  <?php endif; ?>
</div>

<?php include('../templates/footer.php'); ?>
</body>
</html>