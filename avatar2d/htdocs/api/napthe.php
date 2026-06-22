<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, menhgia, loai, tien FROM napthe ORDER BY menhgia ASC LIMIT 100");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['napthe' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>