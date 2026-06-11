<?php
include '../inc/db.php';
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $songName = $_POST['song_name'];
    $artistName = $_POST['artist_name'];
    $genre = $_POST['genre'];

    // Thư mục lưu file
    $coverDir = 'uploads/covers/';
    $audioDir = 'uploads/audio/';
    if (!is_dir($coverDir)) mkdir($coverDir, 0755, true);
    if (!is_dir($audioDir)) mkdir($audioDir, 0755, true);

    // ✅ Xử lý ảnh bìa từ base64
    $coverPath = null;
    if (!empty($_POST['cropped_image_data'])) {
        $base64 = explode(',', $_POST['cropped_image_data'])[1];
        $imageData = base64_decode($base64);
        $fileName = $coverDir . time() . '_cropped.jpg';
        file_put_contents($fileName, $imageData);
        $coverPath = $fileName;
    }

    // ✅ Xử lý file nhạc hoặc URL
    $audioPath = null;
    
    if ($_POST['audio_mode'] === 'upload' && !empty($_FILES['audio_file']['tmp_name'])) {
        $audioName = time() . '_' . basename($_FILES['audio_file']['name']);
        $audioPath = $audioDir . $audioName;
        move_uploaded_file($_FILES['audio_file']['tmp_name'], $audioPath);
    } elseif ($_POST['audio_mode'] === 'url' && !empty($_POST['audio_url'])) {
        $audioURL = trim($_POST['audio_url']);
        if (substr($audioURL, -4) !== '.mp3') {
            die("⚠️ Link nhạc phải kết thúc bằng .mp3");
        }
        $audioPath = $audioURL;
    } else {
        die("⚠️ Vui lòng chọn hoặc nhập file nhạc hợp lệ!");
    }

    // ✅ Lưu vào CSDL
    $stmt = $conn->prepare("INSERT INTO songs (title, artist, genre, file_path, cover_path, uploaded_time) VALUES (?, ?, ?, ?, ?, NOW())");
    $stmt->execute([$songName, $artistName, $genre, $audioPath, $coverPath]);

    $_SESSION['last_upload'] = [
    'title' => $songName,
    'artist' => $artistName,
    'genre' => $genre,
    'cover' => $coverPath,
    'audio' => $audioPath
    ];
    header('Location: upload_success.php');
    exit;
} else {
    echo "Truy cập không hợp lệ!";
}
?>