// Geet Music Player - Simple Player JS

var currentPlaylist = [];
var currentIndex = 0;
var audioElement;
var shuffle = false;
var repeat = false;

// Initialize Audio
function initAudio() {
	audioElement = document.createElement('audio');
	
	audioElement.addEventListener("ended", function() {
		nextSong();
	});
	
	audioElement.addEventListener("timeupdate", function() {
		updateProgress();
	});
}

// Update Progress Bar
function updateProgress() {
	if (audioElement.duration) {
		var progress = (audioElement.currentTime / audioElement.duration) * 100;
		document.querySelector('.progress-bar .progress').style.width = progress + '%';
		
		document.querySelector('.time.current').textContent = formatTime(audioElement.currentTime);
		document.querySelector('.time.remaining').textContent = formatTime(audioElement.duration - audioElement.currentTime);
	}
}

// Format Time
function formatTime(seconds) {
	var mins = Math.floor(seconds / 60);
	var secs = Math.floor(seconds % 60);
	return mins + ':' + (secs < 10 ? '0' : '') + secs;
}

// Play Song
function playSong() {
	if (audioElement && audioElement.src) {
		audioElement.play();
		document.querySelector('.play').style.display = 'none';
		document.querySelector('.pause').style.display = 'block';
	}
}

// Pause Song
function pauseSong() {
	if (audioElement) {
		audioElement.pause();
		document.querySelector('.play').style.display = 'block';
		document.querySelector('.pause').style.display = 'none';
	}
}

// Next Song
function nextSong() {
	if (currentPlaylist.length > 0) {
		currentIndex = (currentIndex + 1) % currentPlaylist.length;
		loadTrack(currentPlaylist[currentIndex]);
	}
}

// Previous Song
function prevSong() {
	if (audioElement.currentTime > 3) {
		audioElement.currentTime = 0;
	} else if (currentPlaylist.length > 0) {
		currentIndex = (currentIndex - 1 + currentPlaylist.length) % currentPlaylist.length;
		loadTrack(currentPlaylist[currentIndex]);
	}
}

// Load Track
function loadTrack(trackId) {
	$.post("includes/handlers/ajax/getSongJson.php", { songId: trackId }, function(data) {
		var track = JSON.parse(data);
		
		if (track && track.path) {
			audioElement.src = track.path;
			
			// Update UI
			document.querySelector('.now-playing-cover').src = 'assets/images/icons/logo.png';
			document.querySelector('.now-playing-title').textContent = track.title || 'Unknown';
			document.querySelector('.now-playing-artist').textContent = 'Artist';
			
			document.getElementById('nowPlayingBar').style.display = 'grid';
			
			playSong();
		}
	});
}

// Set Track (called from pages)
function setTrack(trackId, playlist, play) {
	if (!audioElement) {
		initAudio();
	}
	
	currentPlaylist = playlist || [trackId];
	currentIndex = currentPlaylist.indexOf(trackId);
	
	if (currentIndex === -1) {
		currentIndex = 0;
	}
	
	loadTrack(currentPlaylist[currentIndex]);
	
	if (play) {
		playSong();
	}
}

// Shuffle
function setShuffle() {
	shuffle = !shuffle;
	document.querySelector('.shuffle').style.opacity = shuffle ? '1' : '0.7';
}

// Repeat
function setRepeat() {
	repeat = !repeat;
	document.querySelector('.repeat').style.opacity = repeat ? '1' : '0.7';
}

// Mute
function setMute() {
	audioElement.muted = !audioElement.muted;
}

// Seek
function seek(event) {
	if (audioElement.duration) {
		var bar = event.currentTarget;
		var rect = bar.getBoundingClientRect();
		var percent = (event.clientX - rect.left) / rect.width;
		audioElement.currentTime = percent * audioElement.duration;
	}
}

// Set Volume
function setVolume(event) {
	var bar = event.currentTarget;
	var rect = bar.getBoundingClientRect();
	var percent = (event.clientX - rect.left) / rect.width;
	audioElement.volume = Math.max(0, Math.min(1, percent));
	
	bar.querySelector('.progress').style.width = (percent * 100) + '%';
}

// Keyboard Shortcuts
document.addEventListener('keydown', function(e) {
	if (e.target.tagName === 'INPUT') return;
	
	switch(e.code) {
		case 'Space':
			e.preventDefault();
			if (document.querySelector('.play').style.display !== 'none') {
				playSong();
			} else {
				pauseSong();
			}
			break;
		case 'ArrowRight':
			nextSong();
			break;
		case 'ArrowLeft':
			prevSong();
			break;
	}
});

// Initialize on load
$(document).ready(function() {
	initAudio();
});
