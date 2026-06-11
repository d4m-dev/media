<?php
include '../inc/db.php';
session_start();

$sort = $_GET['sort'] ?? 'title';
$order = $_GET['order'] ?? 'ASC';
$search = $_GET['search'] ?? '';
$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
$limit = 10;
$offset = ($page - 1) * $limit;

$user_id = $_SESSION['user']['id'] ?? null;
$playlists = [];

if ($user_id) {
    $stmt = $conn->prepare("SELECT id, name FROM playlists WHERE user_id = :user_id");
    $stmt->execute(['user_id' => $user_id]);
    $playlists = $stmt->fetchAll(PDO::FETCH_ASSOC);
}

$search_query = '';
if ($search) {
    $search_query = "AND (title LIKE :search OR artist LIKE :search OR genre LIKE :search)";
}

switch ($sort) {
    case 'genre':
        $order_by = "ORDER BY genre $order";
        break;
    case 'likes':
        $order_by = "ORDER BY like_count DESC";
        break;
    default:
        $order_by = "ORDER BY title $order";
        break;
}

$sql = "SELECT songs.*, 
               (SELECT COUNT(*) FROM favorites WHERE favorites.song_id = songs.id) AS like_count 
        FROM songs 
        WHERE 1=1 $search_query 
        $order_by 
        LIMIT :limit OFFSET :offset";
$stmt = $conn->prepare($sql);
if ($search) $stmt->bindValue(':search', "%$search%");
$stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
$stmt->bindValue(':offset', $offset, PDO::PARAM_INT);
$stmt->execute();
$songs = $stmt->fetchAll(PDO::FETCH_ASSOC);

$count_sql = "SELECT COUNT(*) FROM songs WHERE 1=1 $search_query";
$stmt = $conn->prepare($count_sql);
if ($search) $stmt->bindValue(':search', "%$search%");
$stmt->execute();
$total_songs = $stmt->fetchColumn();
$total_pages = ceil($total_songs / $limit);

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
  <title>Danh Sách Bài Hát</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
  <style>
    .card { transition: all 0.3s ease; cursor: pointer; position: relative; padding: 10px; background: linear-gradient(to right, #fdfbfb, #ebedee);}
    .card:hover { transform: translateY(-10px); }
    .modal { display: none; position: fixed; inset: 0; background: rgba(0, 0, 0, 0.5); justify-content: center; align-items: center; z-index: 999; }
    .modal-content { background: white; padding: 20px; border-radius: 8px; width: calc(100% - 10px); max-width: 400px; margin: 0 5px; animation: fadeIn 0.4s ease-in-out; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
    .close { position: absolute; top: 10px; right: 15px; cursor: pointer; font-size: 20px; color: gray; }
    .btn-custom { color: green; border: none; background: transparent; padding: 6px 12px; border-radius: 50%; font-size: 20px; transition: all 0.3s; }
    .btn-custom:hover { background-color: #a3d9a5; }
    .button-wrapper { position: absolute; bottom: 10px; right: 10px; display: flex; gap: 8px; }
    .search-container, .sort-container { display: flex; justify-content: space-between; margin-bottom: 20px; }
    .search-container input, .search-container button, .sort-container select { height: 40px; }
    .sort-container select { width: 100%; padding: 10px 15px; }
  </style>
</head>
<body class="bg-white">
<?php include('../templates/header.php'); ?>
<header class="bg-green-500 p-4 text-white text-center text-2xl font-bold">Danh Sách Bài Hát</header>
<section class="ml-[10px] mt-8 mx-auto max-w-screen-xl">
  <div class="search-container">
    <form method="GET" action="song.php" class="flex items-center w-full">
      <input type="text" name="search" value="<?= htmlspecialchars($search) ?>" placeholder="Tìm kiếm bài hát..." class="p-2 border rounded-md w-full focus:outline-none focus:ring-2 focus:ring-green-200 focus:border-transparent">
      <button type="submit" class="ml-2 bg-green-500 text-white px-4 py-2 rounded-md whitespace-nowrap focus:outline-none hover:bg-green-600 transition-colors mr-[10px]">Tìm kiếm</button>
    </form>
  </div>
  <div class="w-1/2 rounded-md mt-4">
    <a class="text-xl text-black">Sắp xếp</a>
    <div class="sort-container">
      <form method="GET" action="song.php" class="w-full">
        <input type="hidden" name="search" value="<?= htmlspecialchars($search) ?>">
        <select name="sort" onchange="this.form.submit()" class="p-2 border rounded-md w-full">
          <option value="title" <?= $sort === 'title' ? 'selected' : '' ?>>Tên bài hát (A-Z)</option>
          <option value="genre" <?= $sort === 'genre' ? 'selected' : '' ?>>Thể loại (A-Z)</option>
          <option value="likes" <?= $sort === 'likes' ? 'selected' : '' ?>>Lượt yêu thích (⇅)</option>
        </select>
      </form>
    </div>
  </div>
</section>
<section class="mt-8 mb-10 mx-auto max-w-screen-xl">
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mx-2">
    <?php foreach ($songs as $song): ?>
      <div class="card p-4 border rounded-lg shadow-lg flex items-center space-x-4 relative">
        <a href="player.php?id=<?= $song['id'] ?>" class="flex items-center w-full">
          <div class="flex items-center w-full">
            <img src="<?= $song['cover_path'] ?>" alt="Cover Image" class="w-1/3 h-32 object-cover rounded-md">
            <div class="flex-1 ml-2">
              <h3 class="font-semibold text-lg"><?= htmlspecialchars($song['title']) ?></h3>
              <p class="text-gray-500"><?= htmlspecialchars($song['artist']) ?></p>
              <p class="text-gray-400">Thể loại: <?= htmlspecialchars($song['genre']) ?></p>
              <!-- Hiển thị Lượt thích và Lượt nghe -->
              <p class="text-gray-400">Lượt yêu thích: <?= $song['like_count'] ?? 0 ?></p>
              <p class="text-gray-400">Lượt nghe: <?= $song['views'] ?? 0 ?></p> <!-- Thêm Lượt nghe -->
            </div>
          </div>
        </a>
        <div class="button-wrapper">
          <button class="btn-custom" onclick="openModal(<?= $song['id'] ?>)"><i class="bi bi-plus-circle"></i></button>

          <!-- Kiểm tra nếu người dùng có gói premium -->
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
          
          <!-- Thêm vào yêu thích -->
          <button onclick="submitAddToPlaylist(<?= $song['id'] ?>)" class="w-full bg-green-500 text-white px-4 py-2 rounded hover:bg-green-500 mb-3">🎶Thêm vào Playlist</button>
          
          <div class="mb-4">
            <button onclick="addToFavorites(<?= $song['id'] ?>)" class="w-full bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">💗Thêm vào yêu thích</button>
          </div>
          
          <p id="msg-<?= $song['id'] ?>" class="text-sm mt-3"></p>
        </div>
      </div>
    <?php endforeach; ?>
  </div>
  <div class="mt-8 text-center">
    <nav>
      <ul class="inline-flex space-x-4">
        <?php for ($i = 1; $i <= $total_pages; $i++): ?>
          <li>
            <a href="song.php?sort=<?= $sort ?>&order=<?= $order ?>&search=<?= htmlspecialchars($search) ?>&page=<?= $i ?>" class="px-4 py-2 border border-gray-300 rounded-md <?= $i == $page ? 'bg-green-500 text-white' : 'text-gray-700' ?>"><?= $i ?></a>
          </li>
        <?php endfor; ?>
      </ul>
    </nav>
  </div>
</section>
<script>
function openModal(id) {
  const modal = document.getElementById('modal-' + id);
  const overlay = document.createElement('div');
  overlay.classList.add('modal-overlay');
  document.body.appendChild(overlay);

  modal.classList.remove('hidden');
  modal.classList.add('flex');
}

function closeModal(id) {
  const modal = document.getElementById('modal-' + id);
  const overlay = document.querySelector('.modal-overlay');
  if (overlay) overlay.remove();

  modal.classList.add('hidden');
  modal.classList.remove('flex');
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
</script>
<?php include('../templates/menu.php'); ?>
<?php include('../templates/footer.php'); ?>
</body>
</html>