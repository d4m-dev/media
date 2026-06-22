<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, tennhiemvu, chitiet, phanthuong, hoanthanh FROM nhiemvu ORDER BY id ASC LIMIT 50");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['nhiemvu' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>