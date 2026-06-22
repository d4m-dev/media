<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, user_id, soluong, id_shop FROM vatpham WHERE soluong > 0 LIMIT 100");
$vatpham = [];

while ($row = $result->fetch_assoc()) {
    $vatpham[] = $row;
}

echo json_encode(['vatpham' => $vatpham], JSON_UNESCAPED_UNICODE);
$conn->close();
?>