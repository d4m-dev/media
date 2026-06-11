<?php
session_start();
if (!isset($_SESSION['last_upload'])) {
  header('Location: upload.php');
  exit;
}
$data = $_SESSION['last_upload'];
unset($_SESSION['last_upload']);
?>

<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Đăng Bài Thành Công</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background: #f5f7fa;
    }
    .card {
      max-width: 600px;
      margin: 60px auto;
      border: none;
      border-radius: 12px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }
    .card img {
      border-top-left-radius: 12px;
      border-top-right-radius: 12px;
      max-height: 320px;
      object-fit: cover;
    }
    audio {
      width: 100%;
      margin-top: 10px;
    }
  </style>
</head>
<body>
  <div class="card">
    <?php if (preg_match('/^http/', $data['cover'])): ?>
      <img src="<?= htmlspecialchars($data['cover']) ?>" class="card-img-top" alt="Ảnh bìa">
    <?php else: ?>
      <img src="<?= htmlspecialchars($data['cover']) ?>" class="card-img-top" alt="Ảnh bìa">
    <?php endif; ?>
    <div class="card-body">
      <h4 class="card-title"><?= htmlspecialchars($data['title']) ?></h4>
      <p class="card-text"><strong>Ca sĩ:</strong> <?= htmlspecialchars($data['artist']) ?></p>
      <p class="card-text"><strong>Thể loại:</strong> <?= htmlspecialchars($data['genre']) ?></p>

      <?php if (preg_match('/\.mp3$/', $data['audio'])): ?>
        <audio controls>
          <source src="<?= htmlspecialchars($data['audio']) ?>" type="audio/mpeg">
          Trình duyệt không hỗ trợ audio.
        </audio>
      <?php else: ?>
        <p><strong>Link nhạc:</strong> <a href="<?= htmlspecialchars($data['audio']) ?>" target="_blank"><?= htmlspecialchars($data['audio']) ?></a></p>
      <?php endif; ?>
    </div>
    <div class="text-center mb-4">
      <a href="upload.php" class="btn btn-primary">🎶 Upload tiếp bài mới</a>
    </div>
  </div>
</body>
</html>