<?php
include '../inc/db.php';
session_start();

if (!isset($_SESSION['user'])) {
  http_response_code(401);
  echo json_encode(['error' => 'Chưa đăng nhập']);
  exit;
}

$user_id = $_SESSION['user']['id'];
$data = json_decode(file_get_contents('php://input'), true);
$song_id = intval($data['id'] ?? 0);
$action = $data['action'] ?? '';

if (!$song_id || !in_array($action, ['like', 'dislike'])) {
  http_response_code(400);
  echo json_encode(['error' => 'Dữ liệu không hợp lệ']);
  exit;
}

// Kiểm tra reaction cũ
$stmt = $conn->prepare("SELECT reaction FROM song_reactions WHERE user_id = ? AND song_id = ?");
$stmt->execute([$user_id, $song_id]);
$existing = $stmt->fetch(PDO::FETCH_ASSOC);

$conn->beginTransaction();

try {
  if (!$existing) {
    // Chưa có, thêm mới
    $conn->prepare("INSERT INTO song_reactions(user_id, song_id, reaction) VALUES (?, ?, ?)")
         ->execute([$user_id, $song_id, $action]);

    $conn->prepare("UPDATE songs SET {$action}s = {$action}s + 1 WHERE id = ?")->execute([$song_id]);
  } elseif ($existing['reaction'] === $action) {
    // Đã có cùng reaction → gỡ
    $conn->prepare("DELETE FROM song_reactions WHERE user_id = ? AND song_id = ?")
         ->execute([$user_id, $song_id]);

    $conn->prepare("UPDATE songs SET {$action}s = {$action}s - 1 WHERE id = ?")->execute([$song_id]);
  } else {
    // Đã có phản ứng ngược → đổi chiều
    $conn->prepare("UPDATE song_reactions SET reaction = ? WHERE user_id = ? AND song_id = ?")
         ->execute([$action, $user_id, $song_id]);

    $conn->prepare("UPDATE songs SET likes = likes + " . ($action === 'like' ? 1 : -1) . ",
                                   dislikes = dislikes + " . ($action === 'dislike' ? 1 : -1) . "
                    WHERE id = ?")->execute([$song_id]);
  }

  $conn->commit();

  // Trả lại số lượt mới
  $stmt = $conn->prepare("SELECT likes, dislikes FROM songs WHERE id = ?");
  $stmt->execute([$song_id]);
  $count = $stmt->fetch(PDO::FETCH_ASSOC);

  echo json_encode(['success' => true] + $count);
} catch (Exception $e) {
  $conn->rollBack();
  http_response_code(500);
  echo json_encode(['error' => 'Lỗi server']);
}