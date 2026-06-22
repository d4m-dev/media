<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, tenvatpham, gia, loaitien, gioitinh, timesudung FROM shopdo WHERE hienthi = 1 LIMIT 100");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['shopdo' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>