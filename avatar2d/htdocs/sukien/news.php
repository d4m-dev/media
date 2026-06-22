<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, time, avt, name, text FROM news ORDER BY time DESC LIMIT 20");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['news' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>