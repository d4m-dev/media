<?php
	ob_start();
	session_start();

	$timezone = date_default_timezone_set("Asia/Ho_Chi_Minh");

	$host = '127.0.0.1';
	$port = '3306';
	$dbname = 'musicapp';
	$username = 'root';
	$password = '';

	$con = new mysqli($host, $username, $password, $dbname, $port);

	if(mysqli_connect_errno()) {
		die("Failed to connect to MySQL: " . mysqli_connect_error() . 
		    "<br>Please check if MySQL is running and database '$dbname' exists.");
	}
?>