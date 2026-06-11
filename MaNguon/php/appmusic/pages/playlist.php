<?php
include '../inc/db.php';
session_start();

if (!isset($_SESSION['user'])) {
  header('Location: ../login.php');
  exit;
}

$user_id = $_SESSION['user']['id'];
$_SESSION['csrf_token'] = bin2hex(random_bytes(32)); // Token bảo mật

// Tìm kiếm playlist
$search = trim($_GET['search'] ?? '');
if ($search) {
  $stmt = $conn->prepare("SELECT * FROM playlists WHERE user_id = ? AND name LIKE ?");
  $stmt->execute([$user_id, "%$search%"]);
} else {
  $stmt = $conn->prepare("SELECT * FROM playlists WHERE user_id = ?");
  $stmt->execute([$user_id]);
}
$playlists = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Lấy 4 bài hát ngẫu nhiên
$stmt2 = $conn->query("SELECT * FROM songs ORDER BY RAND() LIMIT 4");
$random_songs = $stmt2->fetchAll(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Playlist của bạn</title>
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
      border-radius: 12px;
      padding: 10px 20px;
      width: 100%;
      max-width: 400px;
      border: 1px solid #38a169;
      outline: none;
    }
    .search-input::placeholder {
      color: #38a169;
    }
    .search-button {
      background-color: #38a169;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 12px;
      margin-left: 10px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
    .search-button:hover {
      background-color: #48bb78;
    }
    .loading-spinner {
      animation: spin 1s linear infinite;
      display: inline-block;
    }
    @keyframes spin {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
  </style>
</head>
<body class="bg-white font-sans">

<?php include('../templates/header.php'); ?>

<div class="container mx-auto max-w-[90%] mt-[20px] pb-[40px]">
  <h2 class="text-black text-center text-2xl font-bold mb-10">🎧 Playlist của bạn</h2>
  <div class="search-container">
    <form class="flex mb-8" method="GET">
      <input class="p-2 border rounded-md w-full focus:outline-none focus:ring-2 focus:ring-green-200 focus:border-transparent" 
           type="search" 
           name="search" 
           placeholder="Tìm playlist..." 
           value="<?= htmlspecialchars($search) ?>">
      <button class="ml-2 bg-green-500 text-white px-4 py-2 rounded-md whitespace-nowrap focus:outline-none hover:bg-green-600 transition-colors mr-[10px]" type="submit">Tìm</button>
    </form>
  </div>

  <?php if (empty($playlists)): ?>
    <div class="text-center py-10">
      <p class="text-gray-500 mb-4">Bạn chưa tạo playlist nào.</p>
      <a href="../pages/create_playlist.php" class="bg-green-500 text-white px-4 py-2 rounded-md inline-block hover:bg-green-600 transition-colors">
        Tạo playlist mới
      </a>
    </div>
  <?php else: ?>
    <div class="space-y-5">
      <?php foreach ($playlists as $p): ?>
        <div class="group bg-gradient-to-r from-[#fdfbfb] to-[#ebedee] rounded-xl shadow-md hover:scale-[1.01] transition-transform h-[50px] flex items-center relative overflow-hidden">
          <!-- Thẻ a bao phủ phần clickable -->
          <a href="../handler/detail_playlist.php?id=<?= $p['id']; ?>" class="absolute inset-0 z-10 w-[calc(100%-80px)]"></a>
          
          <!-- Ảnh playlist -->
          <div class="h-full w-[20%] flex-shrink-0 relative z-20">
            <img src="https://i.postimg.cc/pV5YXTfH/my-playlist.jpg" class="h-full w-full object-cover">
          </div>
          
          <!-- Tên playlist -->
          <div class="flex-1 min-w-0 px-3 relative z-20">
            <h5 class="font-medium text-black truncate">
              <?= htmlspecialchars($p['name']) ?>
            </h5>
          </div>
          
          <!-- Nút xóa -->
          <div class="relative z-30 mr-2">
            <button class="delete-playlist bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-lg text-sm transition-colors"
                    data-id="<?= $p['id']; ?>">
              Xóa
            </button>
          </div>
        </div>
      <?php endforeach; ?>
    </div>
  <?php endif; ?>

  <hr class="my-8 border-white/20">

  <h2 class="text-gray-500 text-center text-2xl font-bold mb-8">🎶 Có Thể Bạn Sẽ Thích</h2>

  <div class="space-y-5">
    <?php foreach ($random_songs as $song): ?>
      <div class="bg-gradient-to-r from-[#fdfbfb] to-[#ebedee] rounded-xl p-5 shadow-md hover:scale-[1.01] transition-transform">
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
</div>

<script>
document.querySelectorAll('.delete-playlist').forEach(btn => {
  btn.addEventListener('click', async function(e) {
    e.stopPropagation();
    e.preventDefault();
    
    if (!confirm('Bạn có chắc muốn xoá playlist này không?')) return;
    
    // Hiển thị loading
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="bi bi-arrow-clockwise loading-spinner mr-1"></i> Đang xóa...';
    
    try {
      const response = await fetch('../handler/delete_playlist.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          id: this.dataset.id,
          csrf_token: '<?= $_SESSION['csrf_token'] ?>'
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        this.closest('.group').remove(); // Xóa card khỏi giao diện
      } else {
        alert(data.error || 'Xóa thất bại');
      }
    } catch (error) {
      console.error('Lỗi:', error);
      alert('Có lỗi xảy ra khi xóa');
    } finally {
      btn.disabled = false;
      btn.innerHTML = originalText;
    }
  });
});
</script>

<?php include('../templates/footer.php'); ?>
<?php include('../templates/menu.php'); ?>
</body>
</html>