<?php
include '../inc/db.php';
session_start();

// Kiểm tra người dùng đã đăng nhập chưa
if (!isset($_SESSION['user'])) {
    header('Location: ../login.php');
    exit;
}

$user_id = $_SESSION['user']['id'];
$plan_name = 'free'; // Mặc định gói free

// Lấy thông tin người dùng
$user_query = "SELECT * FROM users WHERE id = :user_id";
$stmt = $conn->prepare($user_query);
$stmt->bindParam(':user_id', $user_id);
$stmt->execute();
$user = $stmt->fetch(PDO::FETCH_ASSOC);

// Lấy thông tin gói đăng ký của người dùng
$user_subscription_query = "
  SELECT subscription_plans.plan_name 
  FROM user_subscriptions
  JOIN subscription_plans ON user_subscriptions.plan_id = subscription_plans.id
  WHERE user_subscriptions.user_id = :user_id AND user_subscriptions.status = 'active' 
  ORDER BY user_subscriptions.end_date DESC LIMIT 1";

$stmt = $conn->prepare($user_subscription_query);
$stmt->bindParam(':user_id', $user_id);
$stmt->execute();
$user_subscription = $stmt->fetch(PDO::FETCH_ASSOC);

// Kiểm tra gói của người dùng, có thể là "free" hoặc "premium"
if ($user_subscription) {
    $plan_name = $user_subscription['plan_name'];
}

// Lấy danh sách playlist của người dùng
$playlist_query = "SELECT * FROM playlists WHERE user_id = :user_id";
$stmt = $conn->prepare($playlist_query);
$stmt->bindParam(':user_id', $user_id);
$stmt->execute();
$playlists = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Lấy danh sách yêu thích của người dùng
$favorite_query = "SELECT songs.id, songs.title, songs.cover_path FROM favorites 
                    JOIN songs ON favorites.song_id = songs.id 
                    WHERE favorites.user_id = :user_id";
$stmt = $conn->prepare($favorite_query);
$stmt->bindParam(':user_id', $user_id);
$stmt->execute();
$favorites = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Lấy lịch sử nghe nhạc của người dùng
$history_query = "SELECT songs.id, songs.title, songs.cover_path FROM listening_history 
                  JOIN songs ON listening_history.song_id = songs.id 
                  WHERE listening_history.user_id = :user_id";
$stmt = $conn->prepare($history_query);
$stmt->bindParam(':user_id', $user_id);
$stmt->execute();
$history = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Trang Cá Nhân</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/cropperjs/dist/cropper.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/cropperjs/dist/cropper.min.js"></script>

  <style>
    .profile-card { transition: all 0.3s ease; cursor: pointer; position: relative; padding: 20px; background: #f4f4f4; border-radius: 10px; }
    .profile-card:hover { transform: translateY(-10px); }
    .btn-custom { color: green; border: none; background: transparent; padding: 6px 12px; border-radius: 50%; font-size: 20px; transition: all 0.3s; }
    .btn-custom:hover { background-color: #a3d9a5; }
    .section { margin-top: 20px; }
    .playlist-item { display: flex; justify-content: space-between; padding: 8px; background: #f9f9f9; margin-bottom: 10px; border-radius: 5px; }
    .card { white-space: nowrap; text-overflow: ellipsis; max-height: 60px; display: flex; align-items: center; margin-bottom: 10px; background: #f9f9f9; border-radius: 8px; overflow: hidden; }
    .card img { height: 100%; width: 10%; }
    .card-content { padding-left: 15px; flex: 1; }
    .card:hover { transform: scale(1.02); transition: all 0.3s ease; }
    /* CSS cho Modal */
    .modal { display: none; position: fixed; inset: 0; background: rgba(0, 0, 0, 0.5); justify-content: center; align-items: center; z-index: 999; }
    .modal-content { background: white; padding: 20px; border-radius: 8px; width: calc(100% - 10px); max-width: 600px; margin: 0 5px; animation: fadeIn 0.4s ease-in-out; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
    .close { position: absolute; top: 10px; right: 15px; cursor: pointer; font-size: 20px; color: gray; }
    .upload-btn { margin-top: 10px; }
  </style>
</head>
<body class="bg-white">
<?php include('../templates/header.php'); ?>

<!-- Modal upload ảnh -->
<div class="modal" id="uploadModal">
    <div class="modal-content">
        <span class="close" onclick="closeModal()">×</span>
        <h2 class="text-lg font-semibold mb-4">Cập Nhật Ảnh Đại Diện</h2>
        <input type="file" id="imageUpload" accept="image/*" class="p-2 mb-4">
        <div>
            <img id="image" src="" alt="Ảnh đại diện" style="max-width: 100%; display: none;">
        </div>
        <button id="cropButton" class="btn-custom bg-blue-500 text-white px-4 py-2 rounded mt-4">Cập Nhật Ảnh Đại Diện</button>
    </div>
</div>

<!-- Hiển thị thông tin người dùng -->
<div class="container mx-auto p-4">
    <div class="profile-card">
        <h2 class="text-2xl font-semibold mb-4">Thông Tin Cá Nhân</h2>
        <div class="flex items-center">
            <!-- Hiển thị ảnh từ cơ sở dữ liệu -->
            <img src="<?= htmlspecialchars($user['avatar']) ?>" alt="Avatar" class="w-[55px] h-[55px] rounded-full mr-4 object-cover">
            <div>
                <h3 class="text-xl"><?= htmlspecialchars($user['username']) ?></h3>
                <p class="text-gray-600"><?= $user['email'] ?></p>
                <p class="text-gray-600">Gói đăng ký: <strong><?= ucfirst($plan_name) ?></strong></p>
            </div>
        </div>
        <div class="upload-btn">
            <button onclick="openModal()" class="btn-custom bg-blue-500 text-white px-2 py-1 text-sm rounded">Tải Lên</button>
        </div>
    </div>

    <!-- Playlist Của Tôi -->
    <div class="section">
        <h2 class="text-2xl font-semibold mb-4">🎶Playlist Của Tôi</h2>
        <?php foreach ($playlists as $playlist): ?>
            <a href="../pages/detail_playlist.php?id=<?= $playlist['id'] ?>" class="card">
                <img src="https://i.postimg.cc/pV5YXTfH/my-playlist.jpg" alt="Playlist" class="object-cover w-12 h-12">
                <div class="card-content">
                    <p class="text-lg"><?= htmlspecialchars($playlist['name']) ?></p>
                </div>
            </a>
        <?php endforeach; ?>
    </div>

    <!-- Danh Sách Yêu Thích -->
    <div class="section">
        <h2 class="text-2xl font-semibold mb-4">💗Danh Sách Yêu Thích</h2>
        <?php foreach ($favorites as $favorite): ?>
            <a href="../pages/player.php?id=<?= $favorite['id'] ?>" class="card">
                <img src="<?= $favorite['cover_path'] ?: 'https://i.postimg.cc/NFKfcFLC/my-favorite.png' ?>" alt="Song" class="object-cover w-12 h-12">
                <div class="card-content">
                    <p class="text-lg"><?= htmlspecialchars($favorite['title']) ?></p>
                </div>
            </a>
        <?php endforeach; ?>
    </div>

    <!-- Lịch Sử Nghe Nhạc -->
    <div class="section">
        <h2 class="text-2xl font-semibold mb-4">Lịch Sử Nghe Nhạc</h2>
        <?php foreach ($history as $song): ?>
            <a href="../handler/detail_history.php?song_id=<?= $song['id'] ?>" class="card">
                <img src="<?= $song['cover_path'] ?: 'https://via.placeholder.com/50' ?>" alt="Song" class="object-cover w-12 h-12">
                <div class="card-content">
                    <p class="text-lg"><?= htmlspecialchars($song['title']) ?></p>
                </div>
            </a>
        <?php endforeach; ?>
    </div>
</div>
<script>
// JavaScript for Modal & Cropper.js
let cropper;

function openModal() {
    const modal = document.getElementById('uploadModal');
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('uploadModal');
    modal.style.display = 'none';
    if (cropper) {
        cropper.destroy();
    }
}

document.getElementById('imageUpload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const image = document.getElementById('image');
            image.src = e.target.result;
            image.style.display = 'block';

            // Sử dụng Cropper.js để cắt xén ảnh
            if (cropper) {
                cropper.destroy();
            }
            cropper = new Cropper(image, {
                aspectRatio: 1,
                viewMode: 2,
                responsive: true,
            });
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('cropButton').addEventListener('click', function() {
    const canvas = cropper.getCroppedCanvas();
    canvas.toBlob(function(blob) {
        const formData = new FormData();
        formData.append('avatar', blob, 'avatar.png');
        formData.append('submit', true);

        // Gửi ảnh đã cắt tới PHP
        fetch('profile.php', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            alert(data);
            closeModal();
        })
        .catch(error => {
            console.error(error);
            alert('Đã xảy ra lỗi!');
        });
    }, 'image/png');
});
</script>
<?php include('../templates/menu.php'); ?>
<?php include('../templates/footer.php'); ?>
</body>
</html>