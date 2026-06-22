<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, name, gia, img, hp, hpfull, sm, exp, lv FROM shoppkm WHERE check = 0 ORDER BY id ASC LIMIT 100");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['shoppkm' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>