<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, user_id, user_vs, time FROM ranking ORDER BY time DESC LIMIT 100");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['ranking' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>