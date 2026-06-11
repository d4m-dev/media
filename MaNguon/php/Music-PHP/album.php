<?php 
include("includes/includedFiles.php");

if(isset($_GET['id'])) {
	$albumId = $_GET['id'];
} else {
	header("Location: index.php");
}

$album = new Album($con, $albumId);
$artist = $album->getArtist();
?>

<div class="entity-header">
	<img class="entity-image" src="<?php echo $album->getArtworkPath(); ?>" alt="<?php echo $album->getTitle(); ?>">
	<div class="entity-info">
		<div class="entity-type">ALBUM</div>
		<h1 class="entity-name"><?php echo $album->getTitle(); ?></h1>
		<div class="entity-meta">Bởi <?php echo $artist->getName(); ?> • <?php echo $album->getNumberOfSongs(); ?> bài hát</div>
	</div>
</div>

<div class="track-list">
	<?php
	$songIdArray = $album->getSongIds();
	$i = 1;
	
	foreach($songIdArray as $songId) {
		$albumSong = new Song($con, $songId);
		$albumArtist = $albumSong->getArtist();

		echo "<div class='track-item' onclick='setTrack(\"" . $albumSong->getId() . "\", tempPlaylist, true)'>
				<div class='track-number'>
					<span class='trackNumber'>$i</span>
				</div>
				<div class='track-info'>
					<div class='track-title'>" . $albumSong->getTitle() . "</div>
					<div class='track-artist'>" . $albumArtist->getName() . "</div>
				</div>
				<div class='track-duration'>" . $albumSong->getDuration() . "</div>
			</div>";

		$i++;
	}
	?>
</div>

<script>
	var tempSongIds = '<?php echo json_encode($songIdArray); ?>';
	tempPlaylist = JSON.parse(tempSongIds);
</script>