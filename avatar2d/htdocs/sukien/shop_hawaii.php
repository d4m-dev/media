<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, nlb, dmt, kcvt, id_shop, dsh FROM shop_hawaii ORDER BY id DESC LIMIT 100");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['shop_hawaii' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>