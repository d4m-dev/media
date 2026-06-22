<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, code, danhmuc FROM giftcode LIMIT 100");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['giftcode' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>