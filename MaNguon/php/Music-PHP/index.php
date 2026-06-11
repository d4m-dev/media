<?php
include("includes/config.php");
include("includes/classes/User.php");
include("includes/classes/Artist.php");
include("includes/classes/Album.php");
include("includes/classes/Song.php");
include("includes/classes/Playlist.php");

if(isset($_SESSION['userLoggedIn'])) {
	$userLoggedIn = new User($con, $_SESSION['userLoggedIn']);
	$username = $userLoggedIn->getUsername();
} else {
	header("Location: register.php");
	exit();
}
?>

<!DOCTYPE html>
<html lang="vi">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Geet Music Player</title>
	
	<!-- Styles -->
	<link rel="stylesheet" href="assets/css/style-new.css">
	
	<!-- jQuery -->
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
</head>
<body>
	<div class="app-container">
		<!-- Theme Toggle -->
		<button class="theme-toggle" onclick="toggleTheme()" title="Đổi giao diện">
			<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
				<path d="M12 3a9 9 0 109 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 01-4.4 2.26 5.403 5.403 0 01-3.14-9.8c-.44-.06-.9-.1-1.36-.1z"/>
			</svg>
		</button>
		
		<!-- Mobile Menu Button -->
		<button class="mobile-menu-btn" onclick="toggleMobileMenu()">
			<svg viewBox="0 0 24 24">
				<path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
			</svg>
		</button>
		
		<!-- Overlay -->
		<div class="overlay" onclick="toggleMobileMenu()"></div>
		
		<div class="main-content">
			<!-- Sidebar -->
			<aside class="sidebar">
				<div class="sidebar-header">
					<div class="logo" onclick="openPage('browse.php')">
						<img src="assets/images/icons/play.png" alt="Logo">
						<span>Geet</span>
					</div>
				</div>
				
				<nav class="nav-menu">
					<a class="nav-item" onclick="openPage('search.php')">
						<img src="assets/images/icons/search.png" alt="Search">
						Tìm kiếm
					</a>
					<a class="nav-item" onclick="openPage('browse.php')">
						<img src="assets/images/icons/browse.png" alt="Browse">
						Duyệt xem
					</a>
					<a class="nav-item" onclick="openPage('yourMusic.php')">
						<img src="assets/images/icons/playlist.png" alt="Playlists">
						Nhạc của bạn
					</a>
					<a class="nav-item" onclick="openPage('settings.php')">
						<img src="assets/images/icons/user.png" alt="Profile">
						<?php echo $userLoggedIn->getFirstAndLastName(); ?>
					</a>
				</nav>
			</aside>
			
			<!-- Main Content -->
			<main class="content-view">
				<div class="page-content" id="mainContent">
					<!-- Content will be loaded here -->
				</div>
			</main>
		</div>
		
		<!-- Now Playing Bar -->
		<div class="now-playing-bar" id="nowPlayingBar" style="display: none;">
			<div class="now-playing-left">
				<img class="now-playing-cover" src="" alt="Album Art">
				<div class="now-playing-info">
					<div class="now-playing-title"></div>
					<div class="now-playing-artist"></div>
				</div>
			</div>
			
			<div class="player-controls">
				<div class="control-buttons">
					<button class="control-btn shuffle" onclick="setShuffle()" title="Phát ngẫu nhiên">
						<img src="assets/images/icons/shuffle.png" alt="Shuffle">
					</button>
					<button class="control-btn previous" onclick="prevSong()" title="Bài trước">
						<img src="assets/images/icons/previous.png" alt="Previous">
					</button>
					<button class="control-btn play-pause play" onclick="playSong()" title="Phát">
						<img src="assets/images/icons/play.png" alt="Play">
					</button>
					<button class="control-btn play-pause pause" onclick="pauseSong()" title="Tạm dừng" style="display: none;">
						<img src="assets/images/icons/pause.png" alt="Pause">
					</button>
					<button class="control-btn next" onclick="nextSong()" title="Bài tiếp theo">
						<img src="assets/images/icons/next.png" alt="Next">
					</button>
					<button class="control-btn repeat" onclick="setRepeat()" title="Lặp lại">
						<img src="assets/images/icons/repeat.png" alt="Repeat">
					</button>
				</div>
				
				<div class="progress-container">
					<span class="time current">0:00</span>
					<div class="progress-bar" onclick="seek(event)">
						<div class="progress"></div>
					</div>
					<span class="time remaining">0:00</span>
				</div>
			</div>
			
			<div class="volume-control">
				<button class="control-btn volume" onclick="setMute()" title="Âm lượng">
					<img src="assets/images/icons/volume.png" alt="Volume">
				</button>
				<div class="progress-bar volume-bar" onclick="setVolume(event)">
					<div class="progress" style="width: 70%"></div>
				</div>
			</div>
		</div>
	</div>
	
	<script>
		var userLoggedIn = '<?php echo $username; ?>';
		
		// Theme Toggle
		function toggleTheme() {
			const current = document.documentElement.getAttribute('data-theme');
			document.documentElement.setAttribute('data-theme', current === 'light' ? 'dark' : 'light');
			localStorage.setItem('theme', document.documentElement.getAttribute('data-theme'));
		}
		
		// Load saved theme
		const savedTheme = localStorage.getItem('theme') || 'dark';
		document.documentElement.setAttribute('data-theme', savedTheme);
		
		// Mobile Menu
		function toggleMobileMenu() {
			document.querySelector('.sidebar').classList.toggle('open');
			document.querySelector('.overlay').style.display = 
				document.querySelector('.sidebar').classList.contains('open') ? 'block' : 'none';
		}
		
		// Open Page
		function openPage(url) {
			if (window.innerWidth <= 768) {
				toggleMobileMenu();
			}
			
			if(url.indexOf("?") == -1) {
				url = url + "?";
			}
			var encodedUrl = encodeURI(url + "&userLoggedIn=" + userLoggedIn);
			$("#mainContent").load(encodedUrl);
			history.pushState(null, null, url);
		}
		
		// Load initial page
		openPage('browse.php');
	</script>
	
	<script src="assets/js/player.js"></script>
</body>
</html>
