<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, name, info, kg_min, kg_max, cena, soluong FROM fish_r ORDER BY id ASC LIMIT 100");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['fish_r' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>