<?php
// Kiểm tra xem người dùng có đăng nhập không
session_start();
$user_name = isset($_SESSION['user']) ? $_SESSION['user']['username'] : 'Khách';

$path_to_favicon = "https://i.postimg.cc/1R0DrrkW/music.png";
echo '<link rel="icon" href="' . $path_to_favicon . '" type="image/x-icon">';
?>
<div class="bg-white py-4 px-2 rounded-lg shadow-xl text-[#191414] mb-1 text-center">
    <div class="flex justify-between items-center flex-row gap-5">
        <a href="../index.php" class="flex items-center">
            <img src="https://i.postimg.cc/0jr2Dj9Y/logo-icon.png" alt="Icon" class="w-12 h-12 max-w-[48px] max-h-[48px] object-contain">
        </a>
        <p class="text-[#191414] text-sm whitespace-nowrap">Xin chào, <?php echo htmlspecialchars($user_name); ?>!</p>

        <div class="flex gap-2 flex-nowrap">
            <?php if (isset($_SESSION['user'])): ?>
                <a href="../logout.php" class="ml-1 bg-green-500 text-white px-2 py-2 rounded-md whitespace-nowrap focus:outline-none hover:bg-green-600 transition-colors">Đăng xuất</a>
                <?php if ($_SESSION['user']['role'] == 'admin'): ?>
                    <a href="../admin/upload.php" class="ml-1 bg-green-500 text-white px-2 py-2 rounded-md whitespace-nowrap focus:outline-none hover:bg-green-600 transition-colors">Upload</a>
                <?php endif; ?>
            <?php else: ?>
                <a href="../login.php" class="ml-1 bg-green-500 text-white px-2 py-2 rounded-md whitespace-nowrap focus:outline-none hover:bg-green-600 transition-colors">Đăng nhập</a>
                <a href="../register.php" class="ml-1 bg-green-500 text-white px-2 py-2 rounded-md whitespace-nowrap focus:outline-none hover:bg-green-600 transition-colors">Đăng ký</a>
            <?php endif; ?>
        </div>
    </div>
</div>