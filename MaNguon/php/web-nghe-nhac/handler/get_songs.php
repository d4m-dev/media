<?php
include '../inc/db.php';
header('Content-Type: application/json');

if (!isset($_GET['id'])) {
    echo json_encode(['success' => false, 'message' => 'Thiếu ID bài hát']);
    exit;
}

$songId = (int)$_GET['id'];

try {
    $stmt = $conn->prepare("
        SELECT 
            songs.*,
            (SELECT COUNT(*) FROM favorites WHERE song_id = songs.id) AS like_count
        FROM songs 
        WHERE id = :id
    ");
    $stmt->execute(['id' => $songId]);
    $song = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$song) {
        echo json_encode(['success' => false, 'message' => 'Bài hát không tồn tại']);
        exit;
    }

    // Trả về dữ liệu bài hát
    echo json_encode([
        'success' => true,
        'song' => [
            'id' => $song['id'],
            'title' => $song['title'],
            'artist' => $song['artist'],
            'cover_path' => $song['cover_path'],
            'file_path' => $song['file_path'],
            'lyric_path' => $song['lyric_path'] ?? null,
            'like_count' => $song['like_count']
        ]
    ]);
} catch (PDOException $e) {
    echo json_encode(['success' => false, 'message' => 'Lỗi database: ' . $e->getMessage()]);
}