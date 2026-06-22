<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, name, avatar, level, xu, hp, sucmanh FROM users ORDER BY level DESC LIMIT 50");
$users = [];

while ($row = $result->fetch_assoc()) {
    $users[] = $row;
}

echo json_encode(['users' => $users], JSON_UNESCAPED_UNICODE);
$conn->close();
?>