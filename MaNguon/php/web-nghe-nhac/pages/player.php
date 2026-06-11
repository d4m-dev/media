<?php
include '../inc/db.php';
session_start();

if (!isset($_GET['id'])) {
    echo "Bài hát không tồn tại!";
    exit;
}

date_default_timezone_set('Asia/Ho_Chi_Minh');

$song_id = $_GET['id'];

// Lấy bài hát theo ID và số lượt yêu thích, lượt nghe
$stmt = $conn->prepare("SELECT songs.*, 
                        (SELECT COUNT(*) FROM favorites WHERE favorites.song_id = songs.id) AS like_count,
                        songs.views AS view_count
                        FROM songs 
                        WHERE songs.id = :id");
$stmt->bindParam(':id', $song_id, PDO::PARAM_INT);
$stmt->execute();
$song = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$song) {
    echo "Bài hát không tồn tại!";
    exit;
}

// Tăng lượt nghe
$conn->prepare("UPDATE songs SET views = views + 1 WHERE id = :id")
     ->execute([':id' => $song_id]);

// Lấy danh sách tất cả bài cùng thể loại (đã sắp xếp)
$genre = trim($song['genre'] ?? '');
$all_stmt = $conn->prepare("SELECT * FROM songs WHERE genre = :genre ORDER BY uploaded_time");
$all_stmt->execute([':genre' => $genre]);
$genre_songs = $all_stmt->fetchAll(PDO::FETCH_ASSOC);

// Tìm bài kế tiếp trong danh sách
$next_song = null;
for ($i = 0; $i < count($genre_songs); $i++) {
    if ($genre_songs[$i]['id'] == $song_id && isset($genre_songs[$i + 1])) {
        $next_song = $genre_songs[$i + 1];
        break;
    }
}

// Gợi ý thêm bài cùng thể loại
$more_stmt = $conn->prepare("SELECT * FROM songs WHERE genre = :genre AND id != :id ORDER BY uploaded_time DESC LIMIT 10");
$more_stmt->execute([':genre' => $genre, ':id' => $song_id]);
$more_songs = $more_stmt->fetchAll(PDO::FETCH_ASSOC);

// Lấy 3 bài hát ngẫu nhiên
$random_songs_stmt = $conn->prepare("SELECT * FROM songs ORDER BY RAND() LIMIT 3");
$random_songs_stmt->execute();
$random_songs = $random_songs_stmt->fetchAll(PDO::FETCH_ASSOC);

// Thêm bình luận
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['comment_content'])) {
    $comment_content = $_POST['comment_content'];
    $user_id = $_SESSION['user']['id'];

    $comment_stmt = $conn->prepare("INSERT INTO comments (user_id, song_id, content) VALUES (:user_id, :song_id, :content)");
    $comment_stmt->execute([':user_id' => $user_id, ':song_id' => $song_id, ':content' => $comment_content]);
}

// Lấy bình luận của bài hát
$comment_stmt = $conn->prepare("SELECT users.username, comments.content, comments.created_at 
                                FROM comments 
                                JOIN users ON users.id = comments.user_id 
                                WHERE comments.song_id = :song_id 
                                ORDER BY comments.created_at DESC");
$comment_stmt->execute([':song_id' => $song_id]);
$comments = $comment_stmt->fetchAll(PDO::FETCH_ASSOC);

// Chuyển đổi thời gian created_at sang múi giờ Việt Nam và định dạng theo ý muốn
foreach ($comments as &$comment) {
    $comment['created_at'] = date('Y-m-d H:i:s', strtotime($comment['created_at']));
}
?>

<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title><?php echo htmlspecialchars($song['title']); ?></title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    /* Giữ lại các style cần thiết không thể thay thế bằng Tailwind */
    #progress-bar::-webkit-slider-thumb {
      appearance: none;
      width: 12px;
      height: 12px;
      background: #1DB954;
      border-radius: 50%;
      cursor: pointer;
    }
  </style>
</head>
<body class="font-sans bg-white box-border">
  <?php include('../templates/header.php'); ?>

  <div class="text-black text-center">
    <h1 class="m-0 text-3xl font-bold mt-[20px]">Đang Phát:</h1>
  </div>

  <div class="bg-gradient-to-r from-[#fdfbfb] to-[#ebedee] p-8 rounded-2xl shadow-lg w-[80vh] max-w-[380px] text-center backdrop-blur-sm mx-auto mb-10">
    <div class="song-info">
      <img src="<?php echo htmlspecialchars($song['cover_path']); ?>" alt="Cover" class="w-full h-[280px] max-w-[calc(100%-40px)] mx-auto mb-4 object-cover block rounded-xl">
      <h2 class="my-2 mx-0 text-xl text-gray-800"><?php echo htmlspecialchars($song['title']); ?></h2>
      <p class="my-1 mx-0 text-sm text-gray-600"><strong>Ca sĩ:</strong> <?php echo htmlspecialchars($song['artist']); ?></p>
      <p class="my-1 mx-0 text-sm text-gray-600"><strong>Thể loại:</strong> <?php echo htmlspecialchars($song['genre']); ?></p>
      <p class="my-1 mx-0 text-sm text-gray-600"><strong>Lượt yêu thích:</strong> <?php echo htmlspecialchars($song['like_count']); ?></p>
      <p class="my-1 mx-0 text-sm text-gray-600"><strong>Lượt nghe:</strong> <?php echo htmlspecialchars($song['view_count']); ?></p>
    </div>

    <audio id="audio-player" class="hidden">
      <source src="<?php echo htmlspecialchars($song['file_path']); ?>" type="audio/mp3">
      Trình duyệt không hỗ trợ audio.
    </audio>

    <div class="mb-5">
      <input type="range" id="progress-bar" value="0" min="0" step="1" class="w-full h-1.5 rounded appearance-none bg-gray-300 outline-none mb-1.5">
      <div class="text-xs text-gray-500 flex justify-between">
        <span id="current-time">00:00</span> / <span id="duration">00:00</span>
      </div>
    </div>

    <div class="flex justify-center gap-5 mt-2.5">
      <button id="prev-button" class="bg-[#1DB954] text-white border-none text-lg p-3 rounded-full w-12 h-12 cursor-pointer transition-colors duration-300 hover:bg-[#1ED760]">
        <i class="bi bi-skip-start-fill"></i>
      </button>
      <button id="play-pause-button" class="bg-[#1DB954] text-white border-none text-lg p-3 rounded-full w-12 h-12 cursor-pointer transition-colors duration-300 hover:bg-[#1ED760]">
        <i class="bi bi-play-fill"></i>
      </button>
      <button id="next-button" class="bg-[#1DB954] text-white border-none text-lg p-3 rounded-full w-12 h-12 cursor-pointer transition-colors duration-300 hover:bg-[#1ED760]">
        <i class="bi bi-skip-end-fill"></i>
      </button>
    </div>

    <div class="mt-5 text-sm text-gray-700">
      <div class="flex items-center gap-2.5">
        <i class="bi bi-volume-up-fill text-xl" id="volume-icon"></i>
        <input type="range" id="volume" min="0" max="1" step="0.01" value="1" class="flex-1">
        <button id="mute-button" class="bg-none border-none cursor-pointer">
          <i class="bi bi-volume-mute-fill text-xl text-[#1DB954]"></i>
        </button>
      </div>
    </div>
  </div>
  
    <!-- Bình luận -->
  <div class="mt-5 ml-[8px] mr-[8px]">
    <h3 class="font-semibold text-lg">Bình luận</h3>
    <form method="POST">
      <textarea name="comment_content" class="w-full p-2 mt-2 border rounded" placeholder="Thêm bình luận..."></textarea>
      <button type="submit" class="mt-2 bg-[#1DB954] text-white px-4 py-2 rounded">Gửi Bình luận</button>
    </form>
    <div class="mt-4">
      <?php foreach ($comments as $comment): ?>
        <div class="p-2 mb-2 bg-gray-100 rounded">
          <strong><?php echo htmlspecialchars($comment['username']); ?></strong><br>
          <span class="text-sm"><?php echo htmlspecialchars($comment['content']); ?></span><br>
          <span class="text-xs text-gray-500"><?php echo $comment['created_at']; ?></span>
        </div>
      <?php endforeach; ?>
    </div>
  </div>
  
    <!-- Bài hát khác trong thể loại -->
  <div>
    <div class="mt-8 mb-8 text-left">
      <?php if ($more_songs): ?>
        <p class="font-bold">Các bài hát cùng thể loại:</p>
        <div class="grid grid-cols-[repeat(auto-fit,minmax(200px,1fr))] gap-4">
          <?php foreach ($more_songs as $ms): ?>
          <a href="player.php?id=<?php echo $ms['id']; ?>" class="no-underline text-inherit">
            <div class="bg-gradient-to-r from-[#fdfbfb] to-[#ebedee] rounded-lg p-2.5 flex items-center gap-2.5 shadow-sm transition duration-300 hover:shadow-md">
              <img src="<?php echo htmlspecialchars($ms['cover_path']); ?>" alt="cover" class="w-12 h-12 rounded object-cover">
              <div class="text-sm">
                <strong><?php echo htmlspecialchars($ms['title']); ?></strong><br>
                <span class="text-gray-600"><?php echo htmlspecialchars($ms['artist']); ?></span>
              </div>
            </div>
          </a>
          <?php endforeach; ?>
        </div>
      <?php endif; ?>
    </div>
  </div>
  
    <!-- Bài hát bạn có thể thích -->
  <div class="mt-8 mb-8 text-left">
    <p class="font-bold">Bạn có thể thích:</p>
    <div class="grid grid-cols-[repeat(auto-fit,minmax(200px,1fr))] gap-4">
      <?php foreach ($random_songs as $random_song): ?>
        <a href="player.php?id=<?php echo $random_song['id']; ?>" class="no-underline text-inherit">
          <div class="bg-gradient-to-r from-[#fdfbfb] to-[#ebedee] rounded-lg p-2.5 flex items-center gap-2.5 shadow-sm transition duration-300 hover:shadow-md">
            <img src="<?php echo htmlspecialchars($random_song['cover_path']); ?>" alt="cover" class="w-12 h-12 rounded object-cover">
            <div class="text-sm">
              <strong><?php echo htmlspecialchars($random_song['title']); ?></strong><br>
              <span class="text-gray-600"><?php echo htmlspecialchars($random_song['artist']); ?></span>
            </div>
          </div>
        </a>
      <?php endforeach; ?>
    </div>
  </div>
  
  <script>
  // Giữ nguyên phần JavaScript
  const audioPlayer = document.getElementById('audio-player');
  const playPauseButton = document.getElementById('play-pause-button');
  const playPauseIcon = playPauseButton.querySelector('i');
  const prevButton = document.getElementById('prev-button');
  const nextButton = document.getElementById('next-button');
  const volumeControl = document.getElementById('volume');
  const muteButton = document.getElementById('mute-button');
  const volumeIcon = document.getElementById('volume-icon');
  const progressBar = document.getElementById('progress-bar');
  const currentTimeLabel = document.getElementById('current-time');
  const durationLabel = document.getElementById('duration');
  let lastVolume = volumeControl.value;

  function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  audioPlayer.addEventListener('loadedmetadata', () => {
    progressBar.max = Math.floor(audioPlayer.duration);
    durationLabel.textContent = formatTime(audioPlayer.duration);
  });

  audioPlayer.addEventListener('timeupdate', () => {
    progressBar.value = Math.floor(audioPlayer.currentTime);
    currentTimeLabel.textContent = formatTime(audioPlayer.currentTime);
  });

  progressBar.addEventListener('input', () => {
    audioPlayer.currentTime = progressBar.value;
  });

  playPauseButton.addEventListener('click', () => {
    if (audioPlayer.paused) {
      audioPlayer.play();
      playPauseIcon.classList.replace('bi-play-fill', 'bi-pause-fill');
    } else {
      audioPlayer.pause();
      playPauseIcon.classList.replace('bi-pause-fill', 'bi-play-fill');
    }
  });

  volumeControl.addEventListener('input', () => {
    const vol = volumeControl.value;
    audioPlayer.volume = vol;
    if (vol == 0) {
      volumeIcon.className = 'bi bi-volume-mute-fill';
    } else if (vol < 0.5) {
      volumeIcon.className = 'bi bi-volume-down-fill';
    } else {
      volumeIcon.className = 'bi bi-volume-up-fill';
    }
  });

  muteButton.addEventListener('click', () => {
    if (audioPlayer.volume > 0) {
      lastVolume = audioPlayer.volume;
      audioPlayer.volume = 0;
      volumeControl.value = 0;
      volumeIcon.className = 'bi bi-volume-mute-fill';
    } else {
      audioPlayer.volume = lastVolume;
      volumeControl.value = lastVolume;
      volumeIcon.className = lastVolume < 0.5 ? 'bi bi-volume-down-fill' : 'bi bi-volume-up-fill';
    }
  });

  nextButton.addEventListener('click', () => {
    window.location.href = '<?php echo $next_song ? "player.php?id=" . $next_song["id"] : "#"; ?>';
  });

  prevButton.addEventListener('click', () => {
    window.location.href = '<?php echo $prev_song ? "player.php?id=" . $prev_song["id"] : "#"; ?>';
  });
  </script>

  <?php include('../templates/menu.php'); ?>
  <?php include('../templates/footer.php'); ?>
</body>
</html>