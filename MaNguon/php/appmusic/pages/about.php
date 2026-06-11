<?php
include '..inc/db.php';
session_start();
$user_name = isset($_SESSION['user']) ? $_SESSION['user']['username'] : 'Khách';
?>

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trang chủ | Web Nghe Nhạc</title>
    <!--<link rel="stylesheet" href="assets/css/index.css" type="text">-->
<style>
    html, body {
      margin: 0;
      padding: 0;
      font-family: Arial, sans-serif;
      color: #191414;
      background: #FFFFFF;
    }
    
    .about-container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }
    
    .about-header {
      text-align: center;
      margin-bottom: 30px;
    }
    
    .about-header h1 {
      font-size: 3em;
      color: #fff;
      text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    .about-content {
      background: linear-gradient(to right, #fdfbfb, #ebedee);
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
      margin-bottom: 30px;
    }
    
    .about-content h2 {
      font-size: 2.5em;
      text-align: center;
      margin-bottom: 20px;
    }
    
    .about-content p {
      line-height: 1.6;
      font-size: 1.1em;
      margin-bottom: 20px;
    }
    
    .about-content h3 {
      font-size: 2em;
      margin-bottom: 10px;
    }
    
    .about-content ul {
      list-style-type: disc;
      margin-left: 30px;
      font-size: 1.1em;
    }
    
    .about-footer {
      text-align: center;
      margin-top: 50px;
      font-size: 1em;
      color: #fff;
    }
    
    .about-footer p {
      margin: 10px 0;
    }
    
    .listen-btn {
      display: inline-block;
      background-color: #1DB954;
      color: #FFFFFF;
      padding: 15px 30px;
      font-size: 1.2em;
      font-weight: bold;
      text-decoration: none;
      border-radius: 5px;
      margin-top: 10px;
      transition: background-color 0.3s ease;
    }
    
    .listen-btn:hover {
      background-color: #1ED760;
      color: #fff;
    }
    .greeting {
        color: #191414;
        font-size: 1.2rem;
    }
</style>
</head>
<body>
<?php include('../templates/header.php'); ?>

    <div class="about-container">
        <header class="about-header">
            <p class="greeting">Xin chào, <?php echo htmlspecialchars($user_name); ?>!</p>
        </header>
        <section class="about-content">
           <a href="song.php" class="listen-btn">Nghe Nhạc Ngay</a>
            <h2>Về Chúng Tôi</h2>
            <p>Web Nghe Nhạc là nền tảng âm nhạc trực tuyến nơi bạn có thể thưởng thức hàng triệu bài hát, album và playlist yêu thích. Chúng tôi cung cấp một trải nghiệm nghe nhạc tuyệt vời, với giao diện dễ sử dụng và khả năng khám phá âm nhạc mới mỗi ngày.</p>

            <p>Với danh sách phát đa dạng từ các thể loại nhạc như Pop, Rock, EDM, Jazz, Hip-hop đến những album mới nhất từ các nghệ sĩ nổi tiếng, bạn sẽ luôn tìm thấy những bài hát phù hợp với tâm trạng và sở thích của mình.</p>

            <h3>Tính Năng Nổi Bật</h3>
            <ul>
                <li>Danh sách phát được cá nhân hóa theo sở thích của bạn.</li>
                <li>Khám phá nhạc mới mỗi ngày với các album và bài hát mới ra mắt.</li>
                <li>Chất lượng âm thanh cao, mang đến trải nghiệm nghe nhạc sống động.</li>
                <li>Hỗ trợ phát nhạc trực tuyến miễn phí hoặc đăng ký tài khoản VIP để trải nghiệm không quảng cáo.</li>
            </ul>

            <p>Chúng tôi cam kết mang đến cho bạn những trải nghiệm nghe nhạc tuyệt vời nhất với giao diện người dùng thân thiện và dễ sử dụng. Chúc bạn có những giờ phút thư giãn và tận hưởng âm nhạc tuyệt vời tại Web Nghe Nhạc!</p>

            <!-- Nút chuyển đến song.php -->
            <a href="song.php" class="listen-btn">Nghe Nhạc Ngay</a>
        </section>
    </div>
<?php include('../templates/menu.php'); ?>
<?php include('../templates/footer.php'); ?>
</body>
</html>