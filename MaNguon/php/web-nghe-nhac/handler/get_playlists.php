<?php
include '../inc/db.php';
session_start();

if (!isset($_SESSION['user'])) {
    echo json_encode([]);
    exit;
}

$user_id = $_SESSION['user']['id'];
$stmt = $conn->prepare("SELECT id, name FROM playlists WHERE user_id = ?");
$stmt->execute([$user_id]);
$playlists = $stmt->fetchAll(PDO::FETCH_ASSOC);

header('Content-Type: application/json');
echo json_encode($playlists);