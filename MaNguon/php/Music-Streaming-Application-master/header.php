<?php

if (isset($_SESSION)) {
    session_start();
    $logged_in_username = $_SESSION['username'];
}
?>

<div id='section1' align='left'>
    <form name='review' action='searchbox.php' onsubmit='return validateForm()' method='post'>
        <a href='user-dashboard.php'><img src='background.png' alt='HTML5 Icon'></a>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
        <input placeholder='Tìm kiếm' type='text' name='keyword' id='keyword' />
        <input type='submit' name='submit' value='Tìm kiếm' />&emsp;&emsp;&emsp;&emsp;&emsp;
            Xin chào <a href='userprofile.php?uname=<?php echo $logged_in_username; ?>'><?php echo $logged_in_username;?></a>&emsp;&emsp;
            <a href='logout.php'>Đăng xuất</a></form></div>


