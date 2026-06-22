<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, name, hp, sm, rand_1, rand_2, ycsm FROM boss_new ORDER BY id ASC LIMIT 100");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['boss_new' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>