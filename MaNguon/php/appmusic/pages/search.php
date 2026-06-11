<?php
// Bao gồm tệp db.php để kết nối cơ sở dữ liệu
include '../inc/db.php';

session_start();

// Kiểm tra quyền admin và người dùng
$is_admin = isset($_SESSION['user']) && $_SESSION['user']['role'] === 'admin';
$user_id = isset($_SESSION['user']) ? $_SESSION['user']['user_id'] : null;

try {
    // Kết nối cơ sở dữ liệu
    $database = new Database();
    $conn = $database->connect();

    // Truy vấn bài hát có lượt nghe cao nhất
    $query_song = "SELECT * FROM songs ORDER BY views DESC LIMIT 1";
    $stmt_song = $conn->query($query_song);

    // Kiểm tra kết quả truy vấn bài hát
    if ($stmt_song) {
        $top_song = $stmt_song->fetch(PDO::FETCH_ASSOC);
        if (!$top_song) {
            echo "Không tìm thấy bài hát.";
        }
    } else {
        echo "Lỗi trong việc truy vấn bài hát.";
    }

    // Truy vấn playlist của người dùng (nếu có)
    if ($user_id) {
        $query_playlist = "SELECT * FROM playlists WHERE user_id = :user_id";
        $stmt_playlist = $conn->prepare($query_playlist);
        $stmt_playlist->bindParam(':user_id', $user_id, PDO::PARAM_INT);
        $stmt_playlist->execute();
        $playlists = $stmt_playlist->fetchAll(PDO::FETCH_ASSOC);
    } else {
        $playlists = [];
    }

} catch (PDOException $e) {
    error_log("Database connection failed: " . $e->getMessage());
    die("Lỗi kết nối cơ sở dữ liệu. Vui lòng thử lại sau.");
}


$sort = $_GET['sort'] ?? 'title'; // Các giá trị: 'title', 'genre', 'likes'
$search = $_GET['search'] ?? ''; // Tìm kiếm bài hát
$search_query = "";
if ($search) {
    $search_query = "AND (title LIKE :search OR artist LIKE :search OR genre LIKE :search)";
}

?>

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tìm Kiếm</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Thêm custom CSS cho các yêu cầu */
        body {
            background-color: white;
        }

        /* Thiết kế thanh tìm kiếm */
        .search-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            margin-top: 20px;
        }

        .search-input {
            border-radius: 12px; /* Bo góc ô input */
            padding: 10px 20px;
            width: 100%;
            max-width: 400px;
            border: 1px solid #38a169; /* Viền màu xanh lá */
            outline: none;
        }

        .search-input::placeholder {
            color: #38a169; /* Màu chữ placeholder */
        }

        .search-button {
            background-color: #38a169; /* Màu nền nút xanh lá */
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 12px;
            margin-left: 10px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        /* Khi hover, thay đổi thành màu xanh lá nhạt */
        .search-button:hover {
            background-color: #48bb78; /* Màu xanh lá nhạt khi hover */
        }

        /* Thiết kế card */
        .card {
            position: relative;
            border-radius: 12px;
            overflow: hidden;
            height: 200px; /* Chiều cao của card */
            display: block;
        }

        /* Các màu nền khác nhau cho mỗi card */
        .card.bg1 { background-color: #c6f6d5; }
        .card.bg2 { background-color: #fefcbf; }
        .card.bg3 { background-color: #fed7d7; }
        .card.bg4 { background-color: #fef2f2; }
        .card.bg5 { background-color: #c6f6d5; }

        .card img {
            position: absolute;
            top: 50%;
            right: 0;
            height: 40%;
            width: 40%;
            border-radius: 4px;
            object-fit: cover;
            transform: translateY(-50%) rotate(35deg);
        }

        .card .content {
            position: absolute;
            top: 10px;
            left: 10px;
            color: #2d3748;
            z-index: 10;
        }

        .card .content p {
            font-size: 18px;
            font-weight: bold;
        }
    </style>
</head>
<body>
<?php include('../templates/header.php'); ?>
    <!-- Thanh Tìm Kiếm -->
    <div class="search-container">
    <form method="GET" action="song.php" class="flex items-center w-full">
      <input type="text" name="search" value="<?= htmlspecialchars($search) ?>" placeholder="Tìm kiếm bài hát..." class="p-2 ml-[10px] border rounded-md focus:outline-none w-full focus:ring-2 focus:ring-green-200 focus:border-transparent">
      <button type="submit" class="ml-2 bg-green-500 text-white px-4 py-2 rounded-md whitespace-nowrap focus:outline-none hover:bg-green-600 transition-colors mr-[10px]">Tìm kiếm</button>
    </form>
  </div>
<a class="ml-[10px] text-[#2d3748] text-xl font-bold mt-3 mb-2 ">Duyệt tìm tất cả</a>
    <!-- Duyệt Tìm Tất Cả -->
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 p-4">

        <!-- Card Nhạc -->
        <div class="card bg1">
            <a href="song.php" class="block h-full">
                <img src="https://i.postimg.cc/mZCX0nqB/marcela-laskoski-Yrt-Flr-Lo2-DQ-unsplash.jpg" alt="Nhạc">
                <div class="content">
                    <p>Nhạc</p>
                </div>
            </a>
        </div>

        <!-- Card Thể Loại -->
        <div class="card bg2">
            <a href="genre.php" class="block h-full">
                <img src="https://i.postimg.cc/dt9W0ywf/wes-hicks-MEL-j-Jnm7-RQ-unsplash.jpg" alt="Thể Loại">
                <div class="content">
                    <p>Thể Loại</p>
                </div>
            </a>
        </div>

        <!-- Card Playlist -->
        <div class="card bg3">
            <a href="playlist.php" class="block h-full">
                <img src="https://i.postimg.cc/brxmkGbs/adrian-korte-5gn2soe-Ac40-unsplash.jpg" alt="Playlist của tôi">
                <div class="content">
                    <p>Playlist của tôi</p>
                </div>
            </a>
        </div>

        <!-- Card Mới Phát Hành -->
        <div class="card bg4">
            <a href="new_releases.php" class="block h-full">
                <img src="https://i.postimg.cc/cJMx6hk3/chris-yang-o-X-Ry-Hi-CZ-w-unsplash.jpg" alt="Mới Phát Hành">
                <div class="content">
                    <p>Mới Phát Hành</p>
                </div>
            </a>
        </div>

        <!-- Card dành cho Admin (nếu là admin) -->
        <?php if ($is_admin): ?>
            <div class="card bg5">
                <a href="../admin/admin.php" class="block h-full">
                    <img src="https://i.postimg.cc/jdTgKX0N/path-digital-t-R0jvlsm-Cu-Q-unsplash.jpg" alt="Quản lý">
                    <div class="content">
                        <p>Quản lý</p>
                    </div>
                </a>
            </div>
        <?php endif; ?>
    </div>
<?php include('../templates/menu.php'); ?>
<?php include('../templates/footer.php'); ?>
</body>
</html>