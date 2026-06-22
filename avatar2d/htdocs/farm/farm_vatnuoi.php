<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, tenvatnuoi, loai, sotien, ban, banfull FROM farm_vatnuoi LIMIT 50");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['farm_vatnuoi' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>