<?php
include 'inc/db.php';
session_start();

// Lấy danh sách 5 bài hát được nghe nhiều nhất và số lượt thích
$top_songs_query = "
  SELECT songs.*, 
    (SELECT COUNT(*) FROM favorites WHERE favorites.song_id = songs.id) AS like_count 
  FROM songs 
  ORDER BY views DESC LIMIT 5";
$top_songs = $conn->query($top_songs_query)->fetchAll(PDO::FETCH_ASSOC);

// Lấy tất cả bài hát mà không phân trang (hiển thị 3 bài) và số lượt thích
$songs_query = "
  SELECT songs.*, 
    (SELECT COUNT(*) FROM favorites WHERE favorites.song_id = songs.id) AS like_count 
  FROM songs 
  ORDER BY views DESC LIMIT 3";
$songs = $conn->query($songs_query)->fetchAll(PDO::FETCH_ASSOC);

// Lấy tất cả playlist của người dùng đã đăng nhập
$user_id = $_SESSION['user']['id'] ?? null;
$playlists = [];

if ($user_id) {
    $playlists_query = "SELECT id, name FROM playlists WHERE user_id = :user_id";
    $stmt = $conn->prepare($playlists_query);
    $stmt->bindParam(':user_id', $user_id);
    $stmt->execute();
    $playlists = $stmt->fetchAll(PDO::FETCH_ASSOC);
}

// Lấy thông tin gói của người dùng hiện tại
$user_subscription_query = "
  SELECT subscription_plans.plan_name 
  FROM user_subscriptions
  JOIN subscription_plans ON user_subscriptions.plan_id = subscription_plans.id
  WHERE user_subscriptions.user_id = :user_id AND user_subscriptions.status = 'active' 
  ORDER BY user_subscriptions.end_date DESC LIMIT 1";
  
$stmt = $conn->prepare($user_subscription_query);
$stmt->bindParam(':user_id', $_SESSION['user']['id']);
$stmt->execute();
$user_subscription = $stmt->fetch(PDO::FETCH_ASSOC);

// Kiểm tra gói của người dùng, có thể là "free" hoặc "premium"
$plan_name = $user_subscription['plan_name'] ?? 'free'; // Mặc định là 'free'
?>

<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Trang chủ</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
  <style>
    .card { 
      transition: all 0.3s ease; 
      cursor: pointer; 
      position: relative; 
      padding: 10px;
      background: linear-gradient(to right, #fdfbfb, #ebedee);
    }
    .card:hover { transform: translateY(-10px); }

    .btn-custom {
      color: green;
      border: none;
      background: transparent;
      padding: 6px 12px;
      border-radius: 50%;
      font-size: 20px;
      transition: all 0.3s;
    }
    .btn-custom:hover {
      background-color: #a3d9a5;
    }
    .button-wrapper {
      position: absolute;
      bottom: 10px;
      right: 10px;
      display: flex;
      gap: 8px;
    }

    .card img {
      margin-right: 2px;
    }

    .card .flex-1 {
      margin-left: 2px;
    }

    .view-all-btn {
      text-align: center;
      margin-top: 20px;
    }

    /* CSS cho Modal */
    .modal { 
      display: none; 
      position: fixed; 
      inset: 0; 
      background: rgba(0, 0, 0, 0.5); 
      justify-content: center; 
      align-items: center; 
      z-index: 999; 
    }

    .modal-content { 
      background: white; 
      padding: 20px; 
      border-radius: 8px; 
      width: calc(100% - 10px); 
      max-width: 400px; 
      margin: 0 5px; 
      animation: fadeIn 0.4s ease-in-out; 
    }

    @keyframes fadeIn { 
      from { opacity: 0; transform: translateY(-10px); } 
      to { opacity: 1; transform: translateY(0); } 
    }

    .close { 
      position: absolute; 
      top: 10px; 
      right: 15px; 
      cursor: pointer; 
      font-size: 20px; 
      color: gray; 
    }
  </style>
<?php include('templates/header.php'); ?>
</head>
<body class="bg-white">

  <!-- Header -->
  <header class="bg-green-500 p-4 text-white text-center text-2xl">
    <h1>Chào mừng đến với trang nhạc</h1>
  </header>

  <!-- Top Songs -->
  <section class="mt-8 mx-auto max-w-screen-xl">
    <h2 class="text-2xl font-semibold ml-[8px] mb-4">Top 5 Bài Hát Được Nghe Nhiều Nhất</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mx-2">
      <?php foreach ($top_songs as $song): ?>
        <div class="card p-4 border rounded-lg shadow-lg flex items-center space-x-4 relative">
          <a href="pages/player.php?id=<?= $song['id'] ?>" class="flex items-center w-full">
            <img src="<?= $song['cover_path'] ?>" alt="Cover Image" class="w-1/3 h-32 object-cover rounded-md">
            <div class="flex-1 ml-2">
              <h3 class="font-semibold text-lg"><?= htmlspecialchars($song['title']) ?></h3>
              <p class="text-gray-500"><?= htmlspecialchars($song['artist']) ?></p>
              <!-- Hiển thị Lượt thích bên trên phần Lượt nghe -->
              <p class="text-gray-400">Lượt yêu thích: <?= $song['like_count'] ?></p>
              <p class="text-gray-400">Lượt nghe: <?= $song['views'] ?></p>
            </div>
          </a>

          <!-- Button Wrapper -->
          <div class="button-wrapper">
            <button class="btn-custom" onclick="openModal(<?= $song['id'] ?>)">
              <i class="bi bi-plus-circle"></i>
            </button>
            
            <!-- Chỉ hiển thị nút Download nếu người dùng có gói premium -->
            <?php if ($plan_name == 'premium'): ?>
              <a href="<?= $song['file_path'] ?>" class="btn-custom">
                <i class="bi bi-download"></i>
              </a>
            <?php endif; ?>
          </div>
        </div>

        <!-- Modal -->
        <div id="modal-<?= $song['id'] ?>" class="modal">
          <div class="modal-content relative">
            <span class="close" onclick="closeModal(<?= $song['id'] ?>)">&times;</span>
            <h2 class="text-lg font-semibold mb-4">Chọn Playlist hoặc Thêm vào Yêu Thích</h2>
            <select id="playlist-select-<?= $song['id'] ?>" class="w-full p-2 border rounded mb-4">
              <option value="">-- Chọn playlist --</option>
              <?php foreach ($playlists as $pl): ?>
                <option value="<?= $pl['id'] ?>"><?= htmlspecialchars($pl['name']) ?></option>
              <?php endforeach; ?>
            </select>
            <input type="text" id="playlist-new-<?= $song['id'] ?>" placeholder="Tạo playlist mới" class="w-full p-2 border rounded mb-4">
            
            <!-- Thêm vào playlist và yêu thích -->
            <button onclick="submitAddToPlaylist(<?= $song['id'] ?>)" class="w-full bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 mb-3">🎶Thêm vào Playlist</button>
            
            <div class="mb-4">
              <button onclick="addToFavorites(<?= $song['id'] ?>)" class="w-full bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">💗Thêm vào yêu thích</button>
            </div>
            
            
            <p id="msg-<?= $song['id'] ?>" class="text-sm mt-3"></p>
          </div>
        </div>

      <?php endforeach; ?>
    </div>
  </section>

  <!-- Song List -->
  <section class="mt-8 mb-10 mx-auto max-w-screen-xl">
    <h2 class="text-2xl ml-[8px] font-semibold mb-4">Danh Sách Bài Hát</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-6 mx-2">
      <?php foreach ($songs as $song): ?>
        <div class="card p-4 border rounded-lg shadow-lg flex items-center space-x-4 relative">
          <a href="pages/player.php?id=<?= $song['id'] ?>" class="flex items-center w-full">
            <img src="<?= $song['cover_path'] ?>" alt="Cover Image" class="w-1/3 h-32 object-cover rounded-md">
            <div class="flex-1 ml-2">
              <h3 class="font-semibold text-lg"><?= htmlspecialchars($song['title']) ?></h3>
              <p class="text-gray-500"><?= htmlspecialchars($song['artist']) ?></p>
              <!-- Hiển thị Lượt thích bên trên phần Lượt nghe -->
              <p class="text-gray-400">Lượt thích: <?= $song['like_count'] ?></p>
              <p class="text-gray-400">Lượt nghe: <?= $song['views'] ?></p>
            </div>
          </a>

          <!-- Button Wrapper -->
          <div class="button-wrapper">
            <button class="btn-custom" onclick="openModal(<?= $song['id'] ?>)">
              <i class="bi bi-plus-circle"></i>
            </button>
            
            <!-- Chỉ hiển thị nút Download nếu người dùng có gói premium -->
            <?php if ($plan_name == 'premium'): ?>
              <a href="<?= $song['file_path'] ?>" class="btn-custom">
                <i class="bi bi-download"></i>
              </a>
            <?php endif; ?>
          </div>
        </div>
      <?php endforeach; ?>
    </div>

    <!-- Nút xem tất cả -->
    <div class="view-all-btn">
      <a href="pages/song.php" class="px-4 py-2 border border-gray-300 rounded-md text-green-600 hover:bg-green-100">Xem tất cả bài hát</a>
    </div>
  </section>

  <?php include('templates/menu.php'); ?>

  <script>
    function openModal(id) {
      const modal = document.getElementById('modal-' + id);
      modal.style.display = "flex";
    }

    function closeModal(id) {
      const modal = document.getElementById('modal-' + id);
      modal.style.display = "none";
    }

    function addToFavorites(songId) {
      const msg = document.getElementById('msg-' + songId);

      // Gửi yêu cầu để thêm vào favorites
      fetch('../handler/add_to_favorites.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `song_id=${songId}`
      })
      .then(res => res.text())
      .then(data => {
        msg.textContent = data;
        msg.className = data.includes('thành công') ? 'text-green-500 text-sm mt-3' : 'text-red-500 text-sm mt-3';
        if (data.includes('thành công')) {
          setTimeout(() => closeModal(songId), 1500);
        }
      })
      .catch(() => {
        msg.textContent = 'Đã xảy ra lỗi khi thêm vào yêu thích.';
        msg.className = 'text-red-500 text-sm mt-3';
      });
    }

    function submitAddToPlaylist(songId) {
      const select = document.getElementById('playlist-select-' + songId);
      const newName = document.getElementById('playlist-new-' + songId).value.trim();
      const msg = document.getElementById('msg-' + songId);

      if (!select.value && !newName) {
        msg.textContent = 'Vui lòng chọn hoặc tạo một playlist.';
        msg.className = 'text-red-500 text-sm mt-3';
        return;
      }

      const formData = new URLSearchParams();
      formData.append('song_id', songId);
      if (select.value) formData.append('playlist_id', select.value);
      if (newName) formData.append('new_playlist', newName);

      fetch('../handler/add_to_playlist.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData.toString()
      })
      .then(res => res.text())
      .then(data => {
        msg.textContent = data;
        msg.className = data.includes('thành công') ? 'text-green-500 text-sm mt-3' : 'text-red-500 text-sm mt-3';
        if (data.includes('thành công')) {
          setTimeout(() => closeModal(songId), 1500);
        }
      })
      .catch(() => {
        msg.textContent = 'Đã xảy ra lỗi khi thêm.';
        msg.className = 'text-red-500 text-sm mt-3';
      });
    }
  </script>
<?php include('templates/footer.php'); ?>
</body>
</html>