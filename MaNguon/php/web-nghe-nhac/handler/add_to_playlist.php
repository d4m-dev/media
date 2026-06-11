<?php
include '../inc/db.php';
session_start();

if (!isset($_SESSION['user'])) {
    echo "Bạn cần đăng nhập.";
    exit;
}

$user_id = $_SESSION['user']['id'];
$song_id = $_POST['song_id'] ?? null;
$playlist_id = $_POST['playlist_id'] ?? null;
$new_playlist = trim($_POST['new_playlist'] ?? '');

if (!$song_id || (!is_numeric($song_id))) {
    echo "ID bài hát không hợp lệ.";
    exit;
}

// Nếu tạo mới playlist
if (!$playlist_id && $new_playlist !== '') {
    $stmt = $conn->prepare("INSERT INTO playlists (user_id, name) VALUES (:uid, :name)");
    $stmt->execute(['uid' => $user_id, 'name' => $new_playlist]);
    $playlist_id = $conn->lastInsertId();
}

// Kiểm tra playlist thuộc quyền user
$stmt = $conn->prepare("SELECT id FROM playlists WHERE id = :pid AND user_id = :uid");
$stmt->execute(['pid' => $playlist_id, 'uid' => $user_id]);
if (!$stmt->fetch()) {
    echo "Playlist không tồn tại hoặc không thuộc về bạn.";
    exit;
}

// Kiểm tra trùng bài hát
$stmt = $conn->prepare("SELECT id FROM playlist_items WHERE playlist_id = :pid AND song_id = :sid");
$stmt->execute(['pid' => $playlist_id, 'sid' => $song_id]);
if ($stmt->fetch()) {
    echo "Bài hát đã tồn tại trong playlist.";
    exit;
}

// Thêm vào bảng playlist_items
$stmt = $conn->prepare("INSERT INTO playlist_items (playlist_id, song_id) VALUES (:pid, :sid)");
$stmt->execute(['pid' => $playlist_id, 'sid' => $song_id]);

echo "Đã thêm thành công vào playlist!";