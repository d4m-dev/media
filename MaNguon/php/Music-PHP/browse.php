<?php
include("includes/includedFiles.php");
?>

<h1 class="page-title">Duyệt xem</h1>

<h2 class="section-title">Album ngẫu nhiên</h2>

<div class="grid">
	<?php
		$albumQuery = mysqli_query($con, "SELECT * FROM albums ORDER BY RAND() LIMIT 10");

		while($row = mysqli_fetch_array($albumQuery)) {
			echo "<div class='grid-item' onclick='openPage(\"album.php?id=" . $row['id'] . "\")'>
					<img class='grid-item-image' src='" . $row['artworkPath'] . "' alt='" . $row['title'] . "'>
					<div class='grid-item-title'>" . $row['title'] . "</div>
					<div class='grid-item-subtitle'>Album</div>
				</div>";
		}
	?>
</div>

