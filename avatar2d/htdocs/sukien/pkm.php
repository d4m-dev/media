<?php
require_once '../inc/db.php';

$result = $conn->query("SELECT id, id_user, name, hp, hpfull, sm, exp, lv, img FROM pkmn LIMIT 100");
$data = [];

while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode(['pkmn' => $data], JSON_UNESCAPED_UNICODE);
$conn->close();
?>