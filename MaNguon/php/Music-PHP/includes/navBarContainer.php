<div id="navBarContainer">
	<nav class="navBar">

		<span role="link" tabindex="0" onclick="openPage('index.php')" class="logo">
			<img src="assets/images/icons/logo.png">
			<span>Geet</span>
		</span>


		<div class="group">

			<div class="navItem">
				<span role='link' tabindex='0'
					onclick="openPage('search.php')" class="navItemLink">
					<img src="assets/images/icons/search.png" class="icon" alt="Tìm kiếm">
					Tìm kiếm
				</span>
			</div>

		</div>

		<div class="group">
			<div class="navItem">
				<span role="link" tabindex="0" onclick="openPage('browse.php')" class="navItemLink">
					<img src="assets/images/icons/browse.png" class="icon" alt="Duyệt xem">
					Duyệt xem
				</span>
			</div>

			<div class="navItem">
				<span role="link" tabindex="0" onclick="openPage('yourMusic.php')" class="navItemLink">
					<img src="assets/images/icons/playlist.png" class="icon" alt="Nhạc của bạn">
					Nhạc của bạn
				</span>
			</div>

			<div class="navItem">
				<span role="link" tabindex="0" onclick="openPage('settings.php')" class="navItemLink">
					<img src="assets/images/icons/user.png" class="icon" alt="Tài khoản">
					<?php echo $userLoggedIn->getFirstAndLastName(); ?>
				</span>
			</div>
		</div>

		<div class="group" style="margin-top: auto; padding-top: 20px; border-top: 1px solid var(--glass-border);">
			<div class="navItem" onclick="showSleepTimerMenu()">
				<span class="navItemLink">
					<img src="assets/images/icons/timer.png" class="icon" alt="Hẹn giờ">
					Hẹn giờ ngủ
				</span>
			</div>
		</div>

	</nav>
</div>