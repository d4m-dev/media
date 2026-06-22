<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, user_id, id_shop FROM ruongicon LIMIT 100");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['ruongicon' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>