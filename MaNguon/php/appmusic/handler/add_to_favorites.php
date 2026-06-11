<?php
session_start();
include '../inc/db.php';

if (!isset($_SESSION['user']['id'])) {
    header('Location: ../login.php');
    exit;
}

$user_id = $_SESSION['user']['id'];
$song_id = $_POST['song_id'] ?? null;

if (!$song_id) {
    echo 'Lỗi: Không có bài hát được chọn.';
    exit;
}

// Kiểm tra xem bài hát đã có trong yêu thích chưa
$check_query = "SELECT 1 FROM favorites WHERE user_id = :user_id AND song_id = :song_id";
$stmt = $conn->prepare($check_query);
$stmt->bindParam(':user_id', $user_id);
$stmt->bindParam(':song_id', $song_id);
$stmt->execute();

if ($stmt->rowCount() > 0) {
    echo 'Bài hát đã có trong yêu thích của bạn.';
    exit;
}

// Thêm bài hát vào yêu thích
$insert_query = "INSERT INTO favorites (user_id, song_id) VALUES (:user_id, :song_id)";
$stmt = $conn->prepare($insert_query);
$stmt->bindParam(':user_id', $user_id);
$stmt->bindParam(':song_id', $song_id);
$stmt->execute();

echo 'Thêm vào yêu thích thành công!';