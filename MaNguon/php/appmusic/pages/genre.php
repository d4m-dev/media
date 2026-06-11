<?php
include '../inc/db.php';
session_start();

// Lấy thống kê mỗi thể loại
$stmt = $conn->query("
    SELECT genre,
           COUNT(*) AS song_count,
           SUM(views) AS total_views,
           GROUP_CONCAT(DISTINCT artist ORDER BY artist SEPARATOR '||') AS artists,
           MAX(cover_path) AS any_cover
    FROM songs
    WHERE genre IS NOT NULL AND genre <> ''
    GROUP BY genre
    ORDER BY song_count DESC
");

$genres = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Thể loại âm nhạc</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white font-sans text-gray-800 m-0 p-0">

<?php include('../templates/header.php'); ?>

<div class="container mx-auto px-5 py-8">
  <div class="text-white mb-5 text-center">
    <h2 class="text-2xl font-bold text-black">🎧 Thể loại Âm Nhạc</h2>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <?php foreach ($genres as $g): ?>
      <?php
        $artistList = explode('||', $g['artists']);
        $artistDisplay = implode(', ', array_slice($artistList, 0, 3));
        if (count($artistList) > 3) $artistDisplay .= ' và hơn...';
      ?>
      <a href="../handler/detail_genre.php?genre=<?php echo urlencode($g['genre']); ?>" 
         class="bg-gradient-to-r from-[#fdfbfb] to-[#ebedee] rounded-xl p-5 flex items-center gap-5 no-underline text-inherit shadow-lg transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">
        <img src="<?php echo htmlspecialchars($g['any_cover']); ?>" 
             alt="Ảnh thể loại" 
             class="w-24 h-24 object-cover rounded-xl flex-none">
        <div class="flex-1">
          <h5 class="m-0 mb-1.5 text-lg font-medium"><?php echo htmlspecialchars($g['genre']); ?></h5>
          <p class="my-1 text-sm"><strong>Số bài hát:</strong> <?php echo $g['song_count']; ?></p>
          <p class="my-1 text-sm"><strong>Lượt nghe:</strong> <?php echo number_format($g['total_views']); ?></p>
          <p class="my-1 text-sm"><strong>Ca sĩ:</strong> <?php echo htmlspecialchars($artistDisplay); ?></p>
        </div>
      </a>
    <?php endforeach; ?>
  </div>
</div>

<?php include('../templates/footer.php'); ?>
<?php include('../templates/menu.php'); ?>

</body>
</html>