<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, user_id, id_nv, tiendo, nhanthuong FROM nhiemvu_user WHERE nhanthuong = 0 LIMIT 100");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['nhiemvu_user' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>