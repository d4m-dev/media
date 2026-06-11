<?php
include '../inc/db.php';
session_start();

$genre = trim($_GET['genre'] ?? '');
if (!$genre) {
    echo "Không tìm thấy thể loại!";
    exit;
}

$stmt = $conn->prepare("SELECT * FROM songs WHERE genre = :genre ORDER BY uploaded_time DESC");
$stmt->execute([':genre' => $genre]);
$songs = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Thể loại: <?php echo htmlspecialchars($genre); ?></title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white font-sans text-black m-0 p-0">

<?php include('../templates/header.php'); ?>

<div class="container mx-auto px-5 py-8">
  <div class="text-black mb-5">
    <h2 class="text-2xl font-bold">🎶 Thể loại: <?php echo htmlspecialchars($genre); ?></h2>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <?php foreach ($songs as $song): ?>
      <a href="../pages/player.php?id=<?php echo $song['id']; ?>" 
         class="bg-gradient-to-r from-[#fdfbfb] to-[#ebedee] rounded-xl p-5 shadow-lg no-underline text-inherit flex gap-5 items-center transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">
        <img src="<?php echo htmlspecialchars($song['cover_path']); ?>" 
             alt="Cover" 
             class="w-24 h-24 object-cover rounded-xl flex-none">
        <div class="flex-1">
          <h5 class="m-0 mb-1.5 text-lg font-medium"><?php echo htmlspecialchars($song['title']); ?></h5>
          <p class="my-1 text-sm"><strong>Ca sĩ:</strong> <?php echo htmlspecialchars($song['artist']); ?></p>
          <p class="my-1 text-sm"><strong>Lượt nghe:</strong> <?php echo number_format($song['views']); ?></p>
        </div>
      </a>
    <?php endforeach; ?>
  </div>
</div>

<?php include('../templates/footer.php'); ?>
<?php include('../templates/menu.php'); ?>
</body>
</html>