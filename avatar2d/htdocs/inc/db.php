<?php
$db_host = 'sql207.infinityfree.com';
$db_name = 'if0_39272437_avatar2d';
$db_user = 'if0_39272437';
$db_pass = 'L8gVuCgUWn1qvxQ';
$baotri = 'Đang bảo trì !';

$conn = new mysqli($db_host, $db_user, $db_pass, $db_name);

// Kiểm tra lỗi kết nối
if ($conn->connect_error) {
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['status' => 'error', 'message' => $baotri]);
    exit;
}

// Cấu hình charset
$conn->set_charset('utf8mb4');