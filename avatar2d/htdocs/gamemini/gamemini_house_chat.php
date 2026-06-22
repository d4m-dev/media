<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, user_id, nha_id, text, time, view FROM gamemini_house_chat ORDER BY time DESC LIMIT 50");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['house_chat' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>