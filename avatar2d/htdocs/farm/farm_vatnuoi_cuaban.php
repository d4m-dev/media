<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, user_id, id_vatnuoi, tienhoa, timesong, timechoan FROM farm_vatnuoi_cuaban ORDER BY user_id ASC LIMIT 100");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['vatnuoi_cuaban' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>