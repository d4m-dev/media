<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, tenboss, hp, hpfull, sucmanh FROM langtruyenthuyet_boss WHERE hienthi = 1 ORDER BY id DESC LIMIT 50");
$bosses = [];

while ($row = $result->fetch_assoc()) {
    $bosses[] = $row;
}

echo json_encode(['boss' => $bosses], JSON_UNESCAPED_UNICODE);
$conn->close();
?>