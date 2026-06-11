<?php
include '../inc/db.php';
session_start();

if (!isset($_SESSION['user'])) {
    echo json_encode(['error' => 'Chưa đăng nhập.']);
    exit;
}

$data = json_decode(file_get_contents('php://input'), true);
$playlist_id = $data['id'] ?? null;

if (!$playlist_id) {
    echo json_encode(['error' => 'Không có playlist để xóa.']);
    exit;
}

// Kiểm tra xem playlist có tồn tại không và thuộc về người dùng không
$stmt = $conn->prepare("SELECT * FROM playlists WHERE id = ? AND user_id = ?");
$stmt->execute([$playlist_id, $_SESSION['user']['id']]);
$playlist = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$playlist) {
    echo json_encode(['error' => 'Playlist không tồn tại hoặc không phải của bạn.']);
    exit;
}

// Xóa playlist và các bài hát trong playlist
$conn->beginTransaction();
try {
    // Xóa các bài hát trong playlist
    $stmt = $conn->prepare("DELETE FROM playlist_items WHERE playlist_id = ?");
    $stmt->execute([$playlist_id]);

    // Xóa playlist
    $stmt = $conn->prepare("DELETE FROM playlists WHERE id = ?");
    $stmt->execute([$playlist_id]);

    $conn->commit();
    echo json_encode(['success' => 'Playlist đã được xóa thành công.']);
} catch (Exception $e) {
    $conn->rollBack();
    echo json_encode(['error' => 'Đã xảy ra lỗi khi xóa playlist.']);
}