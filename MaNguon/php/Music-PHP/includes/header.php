<?php
	include("includes/config.php");
	include("includes/classes/User.php");
	include("includes/classes/Artist.php");
	include("includes/classes/Album.php");
	include("includes/classes/Song.php");
	include("includes/classes/Playlist.php");

//session_destroy(); LOGOUT

if(isset($_SESSION['userLoggedIn'])) {
	$userLoggedIn = new User($con, $_SESSION['userLoggedIn']);
	$username = $userLoggedIn->getUsername();
	echo "<script>userLoggedIn = '$username';</script>";
}
else {
	header("Location: register.php");
}

?>

<html>
<head>
	<title>Chào mừng đến với Geet! Điểm đến âm nhạc của bạn</title>
	<link rel="icon" href="../assets/images/icons/play.png" type="image/x-icon"/>
	<link rel="shortcut icon" href="../assets/images/icons/play.png" type="image/x-icon"/>

	<!-- Google Fonts -->
	<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
	
	<!-- Modern CSS -->
	<link rel="stylesheet" type="text/css" href="assets/css/modern-style.css">

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
	<script src="assets/js/modern-player.js"></script>
</head>

<body>
	<!-- Animated Background -->
	<div class="animated-bg"></div>
	
	<!-- Theme Toggle -->
	<button class="theme-toggle" onclick="toggleTheme()" title="Chuyển chế độ sáng/tối"></button>

	<div id="mainContainer">

		<div id="topContainer">

			<?php include("includes/navBarContainer.php"); ?>

			<div id="mainViewContainer">

				<div id="mainContent">