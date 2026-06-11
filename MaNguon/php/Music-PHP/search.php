<?php
include("includes/includedFiles.php");

if(isset($_GET['term'])) {
	$term = urldecode($_GET['term']);
} else {
	$term = "";
}
?>

<div class="search-container">
	<input type="text" class="search-input" value="<?php echo $term; ?>" placeholder="Tìm kiếm nghệ sĩ, album hoặc bài hát..." onfocus="this.value = this.value">
</div>

<script>
$(".search-input").focus();
$(function() {
	$(".search-input").keyup(function() {
		clearTimeout(timer);
		timer = setTimeout(function() {
			var val = $(".search-input").val();
			openPage("search.php?term=" + val);
		}, 1000);
	})
})
</script>

<?php if($term == "") exit(); ?>

<h2 class="section-title">BÀI HÁT</h2>
<div class="track-list">
	<?php
	$songsQuery = mysqli_query($con, "SELECT id FROM Songs WHERE title LIKE '$term%' LIMIT 10");

	if(mysqli_num_rows($songsQuery) == 0) {
		echo "<div class='no-results'>Không tìm thấy bài hát nào</div>";
	} else {
		$songIdArray = array();
		$i = 1;
		
		while($row = mysqli_fetch_array($songsQuery)) {
			array_push($songIdArray, $row['id']);
			$albumSong = new Song($con, $row['id']);
			$albumArtist = $albumSong->getArtist();

			echo "<div class='track-item' onclick='setTrack(\"" . $albumSong->getId() . "\", tempPlaylist, true)'>
					<div class='track-number'>$i</div>
					<div class='track-info'>
						<div class='track-title'>" . $albumSong->getTitle() . "</div>
						<div class='track-artist'>" . $albumArtist->getName() . "</div>
					</div>
					<div class='track-duration'>" . $albumSong->getDuration() . "</div>
				</div>";

			$i++;
		}
	}
	?>
</div>

<script>
	var tempSongIds = '<?php echo json_encode($songIdArray); ?>';
	tempPlaylist = JSON.parse(tempSongIds);
</script>

<h2 class="section-title">NGHỆ SĨ</h2>
<div class="grid">
	<?php
	$artistsQuery = mysqli_query($con, "SELECT id FROM artists WHERE name LIKE '$term%' LIMIT 10");

	if(mysqli_num_rows($artistsQuery) == 0) {
		echo "<div class='no-results'>Không tìm thấy nghệ sĩ nào</div>";
	} else {
		while($row = mysqli_fetch_array($artistsQuery)) {
			$artistFound = new Artist($con, $row['id']);
			echo "<div class='grid-item' onclick='openPage(\"artist.php?id=". $artistFound->getId() . "\")'>
					<div class='grid-item-title'>" . $artistFound->getName() . "</div>
					<div class='grid-item-subtitle'>Nghệ sĩ</div>
				</div>";
		}
	}
	?>
</div>

<h2 class="section-title">ALBUM</h2>
<div class="grid">
	<?php
	$albumQuery = mysqli_query($con, "SELECT * FROM albums WHERE title LIKE '$term%' LIMIT 10");

	if(mysqli_num_rows($albumQuery) == 0) {
		echo "<div class='no-results'>Không tìm thấy album nào</div>";
	} else {
		while($row = mysqli_fetch_array($albumQuery)) {
			echo "<div class='grid-item' onclick='openPage(\"album.php?id=" . $row['id'] . "\")'>
					<img class='grid-item-image' src='" . $row['artworkPath'] . "'>
					<div class='grid-item-title'>" . $row['title'] . "</div>
					<div class='grid-item-subtitle'>Album</div>
				</div>";
		}
	}
	?>
</div>
