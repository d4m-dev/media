<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, tenvatlieu, loainguyenlieu, songuyenlieu, songuyenlieu2, timenau, soxu, diem, type FROM farm_nhabep ORDER BY id ASC LIMIT 50");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['farm_nhabep' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>