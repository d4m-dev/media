<?php
	include("includes/config.php");
	include("includes/classes/Account.php");
	include("includes/classes/Constants.php");

	$account = new Account($con);

	include("includes/handlers/register-handler.php");
	include("includes/handlers/login-handler.php");

	function getInputValue($name) {
		if(isset($_POST[$name])) {
			echo $_POST[$name];
		}
	}
?>

<!DOCTYPE html>
<html lang="vi">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Chào mừng đến với Geet</title>
	<link rel="stylesheet" href="assets/css/style-new.css">
	<style>
		.register-page {
			min-height: 100vh;
			display: flex;
			align-items: center;
			justify-content: center;
			background: linear-gradient(135deg, #121212 0%, #1a1a2e 100%);
			padding: 20px;
		}
		
		.auth-container {
			display: grid;
			grid-template-columns: 1fr 1fr;
			max-width: 900px;
			width: 100%;
			background: var(--bg-secondary);
			border-radius: 16px;
			overflow: hidden;
			box-shadow: 0 24px 48px rgba(0, 0, 0, 0.3);
		}
		
		.auth-form {
			padding: 48px;
		}
		
		.auth-form h2 {
			font-size: 28px;
			margin-bottom: 24px;
		}
		
		.form-group {
			margin-bottom: 20px;
		}
		
		.form-group label {
			display: block;
			margin-bottom: 8px;
			font-size: 13px;
			color: var(--text-secondary);
		}
		
		.form-group input {
			width: 100%;
			padding: 14px 18px;
			background: var(--bg-elevated);
			border: 2px solid transparent;
			border-radius: 8px;
			color: var(--text-primary);
			font-size: 14px;
		}
		
		.form-group input:focus {
			outline: none;
			border-color: var(--accent);
		}
		
		.btn-auth {
			width: 100%;
			padding: 16px;
			background: var(--primary-gradient);
			border: none;
			border-radius: 500px;
			color: #fff;
			font-size: 14px;
			font-weight: 600;
			cursor: pointer;
			text-transform: uppercase;
		}
		
		.switch-form {
			margin-top: 24px;
			text-align: center;
			font-size: 14px;
			color: var(--text-secondary);
		}
		
		.switch-form span {
			color: var(--accent);
			cursor: pointer;
			font-weight: 600;
		}
		
		.auth-info {
			background: linear-gradient(135deg, #1db954 0%, #1ed760 100%);
			padding: 48px;
			display: flex;
			flex-direction: column;
			justify-content: center;
		}
		
		.auth-info h1 {
			font-size: 36px;
			margin-bottom: 16px;
		}
		
		.auth-info h2 {
			font-size: 18px;
			font-weight: 400;
			margin-bottom: 24px;
			opacity: 0.9;
		}
		
		.auth-info ul {
			list-style: none;
		}
		
		.auth-info li {
			padding: 8px 0;
			font-size: 15px;
		}
		
		.auth-info li:before {
			content: "✓ ";
			font-weight: bold;
		}
		
		.error-message {
			color: #ff4757;
			font-size: 12px;
			margin-bottom: 8px;
			display: block;
		}
		
		.form-section {
			display: none;
		}
		
		.form-section.active {
			display: block;
		}
		
		@media (max-width: 768px) {
			.auth-container {
				grid-template-columns: 1fr;
			}
			
			.auth-info {
				display: none;
			}
			
			.auth-form {
				padding: 32px 24px;
			}
		}
	</style>
</head>
<body>
	<div class="register-page">
		<div class="auth-container">
			<div class="auth-form">
				<!-- Login Form -->
				<form id="loginForm" class="form-section active" action="register.php" method="POST">
					<h2>Đăng nhập</h2>
					
					<div class="form-group">
						<?php echo $account->getError(Constants::$loginFailed); ?>
						<label for="loginUsername">Tên đăng nhập</label>
						<input id="loginUsername" name="loginUsername" type="text" placeholder="Ví dụ: bartSimpson" value="<?php getInputValue('loginUsername') ?>" required>
					</div>
					
					<div class="form-group">
						<label for="loginPassword">Mật khẩu</label>
						<input id="loginPassword" name="loginPassword" type="password" placeholder="Mật khẩu của bạn" required>
					</div>
					
					<button type="submit" name="loginButton" class="btn-auth">Đăng nhập</button>
					
					<div class="switch-form">
						Chưa có tài khoản? <span onclick="switchForm('register')">Đăng ký ngay</span>
					</div>
				</form>
				
				<!-- Register Form -->
				<form id="registerForm" class="form-section" action="register.php" method="POST">
					<h2>Đăng ký tài khoản</h2>
					
					<div class="form-group">
						<?php echo $account->getError(Constants::$usernameCharacters); ?>
						<?php echo $account->getError(Constants::$usernameTaken); ?>
						<label for="username">Tên đăng nhập</label>
						<input id="username" name="username" type="text" placeholder="Ví dụ: bartSimpson" value="<?php getInputValue('username') ?>" required>
					</div>
					
					<div class="form-group">
						<?php echo $account->getError(Constants::$firstNameCharacters); ?>
						<label for="firstName">Tên</label>
						<input id="firstName" name="firstName" type="text" placeholder="Ví dụ: Bart" value="<?php getInputValue('firstName') ?>" required>
					</div>
					
					<div class="form-group">
						<?php echo $account->getError(Constants::$lastNameCharacters); ?>
						<label for="lastName">Họ</label>
						<input id="lastName" name="lastName" type="text" placeholder="Ví dụ: Simpson" value="<?php getInputValue('lastName') ?>" required>
					</div>
					
					<div class="form-group">
						<?php echo $account->getError(Constants::$emailsDoNotMatch); ?>
						<?php echo $account->getError(Constants::$emailInvalid); ?>
						<?php echo $account->getError(Constants::$emailTaken); ?>
						<label for="email">Email</label>
						<input id="email" name="email" type="email" placeholder="Ví dụ: bart@gmail.com" value="<?php getInputValue('email') ?>" required>
					</div>
					
					<div class="form-group">
						<label for="email2">Xác nhận email</label>
						<input id="email2" name="email2" type="email" placeholder="Ví dụ: bart@gmail.com" value="<?php getInputValue('email2') ?>" required>
					</div>
					
					<div class="form-group">
						<?php echo $account->getError(Constants::$passwordsDoNoMatch); ?>
						<?php echo $account->getError(Constants::$passwordNotAlphanumeric); ?>
						<?php echo $account->getError(Constants::$passwordCharacters); ?>
						<label for="password">Mật khẩu</label>
						<input id="password" name="password" type="password" placeholder="Mật khẩu của bạn" required>
					</div>
					
					<div class="form-group">
						<label for="password2">Xác nhận mật khẩu</label>
						<input id="password2" name="password2" type="password" placeholder="Xác nhận mật khẩu" required>
					</div>
					
					<button type="submit" name="registerButton" class="btn-auth">Đăng ký</button>
					
					<div class="switch-form">
						Đã có tài khoản? <span onclick="switchForm('login')">Đăng nhập ngay</span>
					</div>
				</form>
			</div>
			
			<div class="auth-info">
				<h1>Nghe nhạc tuyệt vời</h1>
				<h2>Nghe hàng triệu bài hát miễn phí</h2>
				<ul>
					<li>Khám phá âm nhạc bạn sẽ yêu thích</li>
					<li>Tạo danh sách phát của riêng bạn</li>
					<li>Theo dõi các nghệ sĩ yêu thích</li>
				</ul>
			</div>
		</div>
	</div>
	
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
	<script>
		function switchForm(form) {
			if (form === 'register') {
				document.getElementById('loginForm').classList.remove('active');
				document.getElementById('registerForm').classList.add('active');
			} else {
				document.getElementById('registerForm').classList.remove('active');
				document.getElementById('loginForm').classList.add('active');
			}
		}
		
		<?php if(isset($_POST['registerButton'])): ?>
			switchForm('register');
		<?php endif; ?>
	</script>
</body>
</html>
