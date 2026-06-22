<?php
require_once '../inc/db.php';

$id = isset($_GET['id']) ? (int)$_GET['id'] : 0;
$result = $conn->query("SELECT * FROM users WHERE id = $id LIMIT 1");

if ($result && $result->num_rows > 0) {
    $data = $result->fetch_assoc();
    echo json_encode(['user' => $data], JSON_UNESCAPED_UNICODE);
} else {
    echo json_encode(['error' => 'Không tìm thấy người dùng']);
}

$conn->close();
?>