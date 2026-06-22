<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, user_id, level, taisan, name FROM gamemini_house LIMIT 100");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['house' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>