<?php
include '../inc/db.php';
session_start();

header('Content-Type: application/json');

// Kiểm tra đăng nhập
if (!isset($_SESSION['user'])) {
  http_response_code(401);
  echo json_encode(['error' => 'Chưa đăng nhập']);
  exit;
}

$user_id = $_SESSION['user']['id'];
$data = json_decode(file_get_contents('php://input'), true);
$name = trim($data['name'] ?? '');

if (!$name) {
  http_response_code(400);
  echo json_encode(['error' => 'Thiếu tên playlist']);
  exit;
}

try {
  $stmt = $conn->prepare("INSERT INTO playlists (user_id, name) VALUES (?, ?)");
  $stmt->execute([$user_id, $name]);

  $playlist_id = $conn->lastInsertId();
  echo json_encode(['success' => true, 'id' => $playlist_id, 'name' => $name]);
} catch (PDOException $e) {
  http_response_code(500);
  echo json_encode(['error' => 'Lỗi khi tạo playlist']);
}