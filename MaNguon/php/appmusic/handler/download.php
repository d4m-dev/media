<?php
include '../inc/db.php';
session_start();

// ✅ Kiểm tra quyền admin
if (!isset($_SESSION['user']) || $_SESSION['user']['role'] !== 'admin') {
    http_response_code(403);
    exit('Bạn không có quyền tải xuống.');
}

// ✅ Kiểm tra ID bài hát
if (!isset($_GET['id']) || !is_numeric($_GET['id'])) {
    http_response_code(400);
    exit('Thiếu hoặc sai ID bài hát!');
}

$song_id = intval($_GET['id']);

// ✅ Truy vấn file_path từ DB
$stmt = $conn->prepare("SELECT file_path FROM songs WHERE id = ?");
$stmt->execute([$song_id]);
$song = $stmt->fetch(PDO::FETCH_ASSOC);

// ✅ Kiểm tra dữ liệu
if (!$song || empty($song['file_path'])) {
    http_response_code(404);
    exit('Không tìm thấy bài hát hoặc thiếu đường dẫn file.');
}

// ✅ Tăng lượt nghe
$conn->prepare("UPDATE songs SET views = views + 1 WHERE id = ?")->execute([$song_id]);

// ✅ Điều hướng sang link để tải
header("Location: " . $song['file_path']);
exit;