// ========================================
// MODERN MUSIC PLAYER - ENHANCED FEATURES
// ========================================

var currentPlaylist = [];
var shufflePlaylist = [];
var tempPlaylist = [];
var audioElement;
var mouseDown = false;
var currentIndex = 0;
var repeat = false;
var shuffle = false;
var userLoggedIn;
var timer;
var isMiniPlayer = false;
var sleepTimer = null;
var likedSongs = JSON.parse(localStorage.getItem('likedSongs')) || [];
var recentlyPlayed = JSON.parse(localStorage.getItem('recentlyPlayed')) || [];
var playbackHistory = [];

// Initialize when document is ready
$(document).ready(function() {
    initTheme();
    initKeyboardShortcuts();
    initMobileMenu();
    loadLikedSongs();
    updateLikeButton();
});

// Mobile Menu Toggle
function initMobileMenu() {
    // Add hamburger menu button
    if (window.innerWidth <= 768) {
        $('body').prepend(`
            <button class="mobile-menu-toggle" onclick="toggleMobileMenu()" style="
                position: fixed;
                top: 15px;
                left: 15px;
                z-index: 1003;
                width: 44px;
                height: 44px;
                background: var(--dark-surface);
                border: 1px solid var(--glass-border);
                border-radius: 10px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: var(--shadow-lg);
            ">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="var(--text-primary)">
                    <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
                </svg>
            </button>
            <div class="mobile-overlay" onclick="toggleMobileMenu()" style="
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                z-index: 1001;
            "></div>
        `);
    }
}

function toggleMobileMenu() {
    const nav = $('#navBarContainer');
    const overlay = $('.mobile-overlay');
    
    if (nav.hasClass('open')) {
        nav.removeClass('open');
        overlay.fadeOut(200);
        $('body').css('overflow', 'auto');
    } else {
        nav.addClass('open');
        overlay.fadeIn(200);
        $('body').css('overflow', 'hidden');
    }
}

// Handle window resize
$(window).resize(function() {
    if (window.innerWidth > 768) {
        $('#navBarContainer').removeClass('open');
        $('.mobile-overlay').hide();
        $('.mobile-menu-toggle').remove();
    } else if (!$('.mobile-menu-toggle').length) {
        initMobileMenu();
    }
});

// Theme Toggle
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
    showToast(newTheme === 'dark' ? 'Chế độ tối' : 'Chế độ sáng');
}

function updateThemeIcon(theme) {
    const themeBtn = document.querySelector('.theme-toggle');
    if (themeBtn) {
        themeBtn.innerHTML = theme === 'dark' 
            ? '<svg viewBox="0 0 24 24"><path d="M12 3a9 9 0 109 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 01-4.4 2.26 5.403 5.403 0 01-3.14-9.8c-.44-.06-.9-.1-1.36-.1z"/></svg>'
            : '<svg viewBox="0 0 24 24"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58a.996.996 0 00-1.41 0 .996.996 0 000 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37a.996.996 0 00-1.41 0 .996.996 0 000 1.41l1.06 1.06c.39.39 1.03.39 1.41 0a.996.996 0 000-1.41l-1.06-1.06zm1.06-10.96a.996.996 0 000 1.41l-1.06 1.06c-.39.39-1.03.39-1.41 0a.996.996 0 010-1.41l1.06-1.06c.39-.39 1.03-.39 1.41 0zM7.05 18.36a.996.996 0 000 1.41.996.996 0 001.41 0l1.06-1.06c.39-.39.39-1.03 0-1.41s-1.03-.39-1.41 0l-1.06 1.06z"/></svg>';
    }
}

// Keyboard Shortcuts
function initKeyboardShortcuts() {
    $(document).keydown(function(e) {
        // Ignore if typing in input
        if ($(e.target).is('input, textarea')) return;

        switch(e.code) {
            case 'Space':
                e.preventDefault();
                togglePlayPause();
                break;
            case 'ArrowRight':
                e.preventDefault();
                nextSong();
                break;
            case 'ArrowLeft':
                e.preventDefault();
                prevSong();
                break;
            case 'ArrowUp':
                e.preventDefault();
                adjustVolume(0.1);
                break;
            case 'ArrowDown':
                e.preventDefault();
                adjustVolume(-0.1);
                break;
            case 'KeyM':
                e.preventDefault();
                setMute();
                break;
            case 'KeyR':
                e.preventDefault();
                setRepeat();
                break;
            case 'KeyS':
                e.preventDefault();
                setShuffle();
                break;
            case 'KeyL':
                e.preventDefault();
                toggleLike();
                break;
        }
    });
}

function togglePlayPause() {
    if ($('.controlButton.pause').is(':visible')) {
        pauseSong();
    } else {
        playSong();
    }
}

function adjustVolume(delta) {
    const newVolume = Math.max(0, Math.min(1, audioElement.audio.volume + delta));
    audioElement.audio.volume = newVolume;
    updateVolumeProgressBar(audioElement.audio);
    showToast('Âm lượng: ' + Math.round(newVolume * 100) + '%');
}

// Like Song Feature
function toggleLike() {
    const songId = audioElement.currentlyPlaying?.id;
    if (!songId) return;

    const index = likedSongs.indexOf(songId);
    if (index > -1) {
        likedSongs.splice(index, 1);
        showToast('Đã bỏ thích bài hát');
    } else {
        likedSongs.push(songId);
        showToast('Đã thêm vào bài yêu thích');
    }
    
    localStorage.setItem('likedSongs', JSON.stringify(likedSongs));
    updateLikeButton();
}

function updateLikeButton() {
    const songId = audioElement.currentlyPlaying?.id;
    const likeBtn = document.querySelector('.controlButton.like');
    
    if (likeBtn && songId) {
        const isLiked = likedSongs.includes(songId);
        likeBtn.style.opacity = isLiked ? '1' : '0.7';
        likeBtn.querySelector('img').src = isLiked 
            ? 'assets/images/icons/heart-active.png' 
            : 'assets/images/icons/heart.png';
    }
}

function loadLikedSongs() {
    // Load from localStorage
    likedSongs = JSON.parse(localStorage.getItem('likedSongs')) || [];
}

// Recently Played
function addToRecentlyPlayed(songId) {
    const index = recentlyPlayed.indexOf(songId);
    if (index > -1) {
        recentlyPlayed.splice(index, 1);
    }
    recentlyPlayed.unshift(songId);
    if (recentlyPlayed.length > 50) {
        recentlyPlayed.pop();
    }
    localStorage.setItem('recentlyPlayed', JSON.stringify(recentlyPlayed));
}

// Sleep Timer
function setSleepTimer(minutes) {
    if (sleepTimer) {
        clearTimeout(sleepTimer);
        sleepTimer = null;
        showToast('Đã tắt hẹn giờ');
        return;
    }

    const ms = minutes * 60 * 1000;
    sleepTimer = setTimeout(function() {
        pauseSong();
        showToast('Hẹn giờ đã hết. Nhạc đã dừng.');
        sleepTimer = null;
    }, ms);

    showToast('Hẹn giờ: ' + minutes + ' phút');
}

function showSleepTimerMenu() {
    const times = [15, 30, 45, 60, 90];
    let menu = '<div class="sleep-timer-menu">';
    menu += '<h4>Chọn thời gian</h4>';
    times.forEach(time => {
        menu += '<button class="button" onclick="setSleepTimer(' + time + ')">' + time + ' phút</button>';
    });
    if (sleepTimer) {
        menu += '<button class="button" onclick="setSleepTimer(0)">Tắt hẹn giờ</button>';
    }
    menu += '</div>';
    
    showToast('Đang mở menu hẹn giờ...');
    // You can create a modal here
    const minutes = prompt("Nhập số phút (15, 30, 45, 60, 90):");
    if (minutes && !isNaN(minutes)) {
        setSleepTimer(parseInt(minutes));
    }
}

// Mini Player
function toggleMiniPlayer() {
    isMiniPlayer = !isMiniPlayer;
    const miniPlayer = document.querySelector('.mini-player');
    if (miniPlayer) {
        miniPlayer.classList.toggle('active', isMiniPlayer);
    }
    showToast(isMiniPlayer ? 'Đã bật mini player' : 'Đã tắt mini player');
}

// Toast Notifications
function showToast(message) {
    let toast = document.querySelector('.toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.className = 'toast';
        document.body.appendChild(toast);
    }
    
    toast.textContent = message;
    toast.classList.add('show');
    
    setTimeout(function() {
        toast.classList.remove('show');
    }, 3000);
}

// Equalizer Visualization
function createEqualizer() {
    const equalizer = document.createElement('div');
    equalizer.className = 'equalizer';
    for (let i = 0; i < 4; i++) {
        const bar = document.createElement('div');
        bar.className = 'equalizer-bar';
        equalizer.appendChild(bar);
    }
    return equalizer;
}

// Queue Management
var queue = [];
var queueIndex = 0;

function addToQueue(songId) {
    queue.push(songId);
    showToast('Đã thêm vào hàng đợi');
}

function showQueue() {
    if (queue.length === 0) {
        showToast('Hàng đợi trống');
        return;
    }
    showToast('Hàng đợi: ' + queue.length + ' bài');
}

function clearQueue() {
    queue = [];
    queueIndex = 0;
    showToast('Đã xóa hàng đợi');
}

// Volume Boost
function toggleVolumeBoost() {
    const currentGain = audioElement.audio.gain || 1;
    const newGain = currentGain === 1 ? 1.5 : 1;
    
    if (typeof audioElement.audio.gain !== 'undefined') {
        audioElement.audio.gain = newGain;
        showToast(newGain > 1 ? 'Tăng âm lượng 150%' : 'Âm lượng bình thường');
    } else {
        showToast('Trình duyệt không hỗ trợ tăng âm lượng');
    }
}

// Search with Filters
function searchWithFilter(type) {
    const term = $('.searchInput').val();
    if (!term) {
        showToast('Vui lòng nhập từ khóa tìm kiếm');
        return;
    }
    
    let url = 'search.php?term=' + encodeURIComponent(term);
    if (type) {
        url += '&type=' + type;
    }
    openPage(url);
}

// Playback Speed Control
function setPlaybackSpeed(speed) {
    audioElement.audio.playbackRate = speed;
    showToast('Tốc độ: ' + speed + 'x');
}

function cyclePlaybackSpeed() {
    const speeds = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2];
    const currentSpeed = audioElement.audio.playbackRate || 1;
    const currentIndex = speeds.indexOf(currentSpeed);
    const nextIndex = (currentIndex + 1) % speeds.length;
    setPlaybackSpeed(speeds[nextIndex]);
}

// Share Song
function shareSong() {
    const song = audioElement.currentlyPlaying;
    if (!song) return;
    
    const url = window.location.origin + '/album.php?id=' + song.album;
    
    if (navigator.share) {
        navigator.share({
            title: song.title,
            text: 'Nghe bài hát này: ' + song.title,
            url: url
        });
    } else {
        navigator.clipboard.writeText(url);
        showToast('Đã sao chép liên kết');
    }
}

// Update existing functions
$(document).click(function(click) {
    var target = $(click.target);

    if(!target.hasClass("item") && !target.hasClass("optionsButton") && !target.hasClass("controlButton")) {
        hideOptionsMenu();
    }
});

$(window).scroll(function() {
    hideOptionsMenu();
});

$(document).on("change", "select.playlist", function() {
    var select = $(this);
    var playlistId = select.val();
    var songId = select.prev(".songId").val();

    $.post("includes/handlers/ajax/addToPlaylist.php", {playlistId: playlistId, songId: songId})
    .done(function(error) {
        if(error != "") {
            alert(error);
            return;
        }
        hideOptionsMenu();
        select.val("");
        showToast('Đã thêm vào danh sách phát');
    });
});

function updateEmail(emailClass) {
    var emailValue = $("." + emailClass).val();

    $.post("includes/handlers/ajax/updateEmail.php", { email: emailValue, username: userLoggedIn})
    .done(function(response) {
        $("." + emailClass).nextAll(".message").text(response);
        if (response.includes('thành công')) {
            showToast('Cập nhật email thành công');
        }
    });
}

function updatePassword(oldPasswordClass, newPasswordClass1, newPasswordClass2) {
    var oldPassword = $("." + oldPasswordClass).val();
    var newPassword1 = $("." + newPasswordClass1).val();
    var newPassword2 = $("." + newPasswordClass2).val();

    $.post("includes/handlers/ajax/updatePassword.php",
        { oldPassword: oldPassword,
          newPassword1: newPassword1,
          newPassword2: newPassword2,
          username: userLoggedIn })
    .done(function(response) {
        $("." + oldPasswordClass).nextAll(".message").text(response);
        if (response.includes('thành công')) {
            showToast('Cập nhật mật khẩu thành công');
        }
    });
}

function logout() {
    if (confirm('Bạn có chắc chắn muốn đăng xuất?')) {
        $.post("includes/handlers/ajax/logout.php", function() {
            location.reload();
        });
    }
}

function openPage(url) {
    if(timer != null) {
        clearTimeout(timer);
    }

    if(url.indexOf("?") == -1) {
        url = url + "?";
    }
    var encodedUrl = encodeURI(url + "&userLoggedIn=" + userLoggedIn);
    console.log(encodedUrl);
    $("#mainContent").load(encodedUrl);
    $("body").scrollTop(0);
    history.pushState(null, null, url);
}

function removeFromPlaylist(button, playlistId) {
    var songId = $(button).prevAll(".songId").val();

    $.post("includes/handlers/ajax/removeFromPlaylist.php", {playlistId: playlistId, songId: songId})
        .done(function(error) {
            if(error != "") {
                alert(error);
                return;
            }
            openPage("playlist.php?id=" + playlistId);
            showToast('Đã xóa khỏi danh sách phát');
        });
}

function createPlaylist() {
    var popup = prompt("Nhập tên danh sách phát mới:");
    if(popup != null && popup.trim() !== "") {
        $.post("includes/handlers/ajax/createPlaylist.php", {name: popup, username: userLoggedIn})
        .done(function(error) {
            if(error != "") {
                alert(error);
                return;
            }
            openPage("yourMusic.php");
            showToast('Đã tạo danh sách phát: ' + popup);
        });
    }
}

function deletePlaylist(playlistId) {
    if (confirm("Bạn có chắc chắn muốn xóa danh sách phát này?")) {
        $.post("includes/handlers/ajax/deletePlaylist.php", {playlistId: playlistId})
        .done(function(error) {
            if(error != "") {
                alert(error);
                return;
            }
            openPage("yourMusic.php");
            showToast('Đã xóa danh sách phát');
        });
    }
}

function hideOptionsMenu() {
    var menu = $(".optionsMenu");
    if(menu.css("display") != "none") {
        menu.css("display", "none");
    }
}

function showOptionsMenu(button) {
    var songId = $(button).prevAll(".songId").val();
    var menu = $(".optionsMenu");
    menu.find(".songId").val(songId);

    var scrollTop = $(window).scrollTop();
    var elementOffset = $(button).offset().top;
    var top = elementOffset - scrollTop;
    var left = $(button).position().left;

    menu.css({ "top": top + "px", "left": left + "px", "display": "inline" });
}

function formatTime(seconds) {
    var time = Math.round(seconds);
    var minutes = Math.floor(time / 60);
    var seconds = time - (minutes * 60);
    var extraZero = (seconds < 10) ? "0" : "";
    return minutes + ":" + extraZero + seconds;
}

function updateTimeProgressBar(audio) {
    $(".progressTime.current").text(formatTime(audio.currentTime));
    $(".progressTime.remaining").text(formatTime(audio.duration - audio.currentTime));

    var progress = audio.currentTime / audio.duration * 100;
    $(".playbackBar .progress").css("width", progress + "%");
}

function updateVolumeProgressBar(audio) {
    var volume = audio.volume * 100;
    $(".volumeBar .progress").css("width", volume + "%");
}

function playFirstSong() {
    setTrack(tempPlaylist[0], tempPlaylist, true);
}

function Audio() {
    this.currentlyPlaying;
    this.audio = document.createElement('audio');

    this.audio.addEventListener("ended", function() {
        nextSong();
    });

    this.audio.addEventListener("canplay", function() {
        var duration = formatTime(this.duration);
        $(".progressTime.remaining").text(duration);
    });

    this.audio.addEventListener("timeupdate", function() {
        if(this.duration) {
            updateTimeProgressBar(this);
        }
    });

    this.audio.addEventListener("volumechange", function() {
        updateVolumeProgressBar(this);
    });

    this.audio.addEventListener("play", function() {
        addToRecentlyPlayed(this.currentlyPlaying?.id);
        updateLikeButton();
    });

    this.setTrack = function(track) {
        this.currentlyPlaying = track;
        this.audio.src = track.path;
    }

    this.play = function() {
        this.audio.play();
    }

    this.pause = function() {
        this.audio.pause();
    }

    this.setTime = function(seconds) {
        this.audio.currentTime = seconds;
    }
}

function setRepeat() {
    repeat = !repeat;
    var imageName = repeat ? "repeat-active.png" : "repeat.png";
    $(".controlButton.repeat img").attr("src", "assets/images/icons/" + imageName);
    showToast(repeat ? 'Lặp lại: Bật' : 'Lặp lại: Tắt');
}

function setMute() {
    audioElement.audio.muted = !audioElement.audio.muted;
    var imageName = audioElement.audio.muted ? "volume-mute.png" : "volume.png";
    $(".controlButton.volume img").attr("src", "assets/images/icons/" + imageName);
    showToast(audioElement.audio.muted ? 'Đã tắt tiếng' : 'Đã bật tiếng');
}

function setShuffle() {
    shuffle = !shuffle;
    var imageName = shuffle ? "shuffle-active.png" : "shuffle.png";
    $(".controlButton.shuffle img").attr("src", "assets/images/icons/" + imageName);

    if(shuffle == true) {
        shuffleArray(shufflePlaylist);
        currentIndex = shufflePlaylist.indexOf(audioElement.currentlyPlaying.id);
    } else {
        currentIndex = currentPlaylist.indexOf(audioElement.currentlyPlaying.id);
    }
    showToast(shuffle ? 'Phát ngẫu nhiên: Bật' : 'Phát ngẫu nhiên: Tắt');
}

function shuffleArray(a) {
    var j, x, i;
    for(i = a.length; i; i--) {
        j = Math.floor(Math.random() * i);
        x = a[i - 1];
        a[i - 1] = a[j];
        a[j] = x;
    }
}

function setTrack(trackId, newPlaylist, play) {
    if(newPlaylist != currentPlaylist) {
        currentPlaylist = newPlaylist;
        shufflePlaylist = currentPlaylist.slice();
        shuffleArray(shufflePlaylist);
    }

    if(shuffle == true) {
        currentIndex = shufflePlaylist.indexOf(trackId);
    } else {
        currentIndex = currentPlaylist.indexOf(trackId);
    }
    
    pauseSong();

    $.post("includes/handlers/ajax/getSongJson.php", { songId: trackId }, function(data) {
        var track = JSON.parse(data);
        $(".trackName span").text(track.title);

        $.post("includes/handlers/ajax/getArtistJson.php", { artistId: track.artist }, function(data) {
            var artist = JSON.parse(data);
            $(".trackInfo .artistName span").text(artist.name);
            $(".trackInfo .artistName span").attr("onclick", "openPage('artist.php?id=" + artist.id + "')");
        });

        $.post("includes/handlers/ajax/getAlbumJson.php", { albumId: track.album }, function(data) {
            var album = JSON.parse(data);
            $(".content .albumLink img").attr("src", album.artworkPath);
            $(".content .albumLink img").attr("onclick", "openPage('album.php?id=" + album.id + "')");
            $(".trackInfo .trackName span").attr("onclick", "openPage('album.php?id=" + album.id + "')");
        });

        audioElement.setTrack(track);

        if(play == true) {
            playSong();
        }
    });
}

function playSong() {
    if(audioElement.audio.currentTime == 0) {
        $.post("includes/handlers/ajax/updatePlays.php", { songId: audioElement.currentlyPlaying.id });
    }

    $(".controlButton.play").hide();
    $(".controlButton.pause").show();
    audioElement.play();
    
    // Show toast with song info
    const song = audioElement.currentlyPlaying;
    if (song) {
        showToast('Đang phát: ' + song.title);
    }
}

function pauseSong() {
    $(".controlButton.play").show();
    $(".controlButton.pause").hide();
    audioElement.pause();
}

function prevSong() {
    if(audioElement.audio.currentTime >= 3 || currentIndex == 0) {
        audioElement.setTime(0);
    } else {
        currentIndex = currentIndex - 1;
        setTrack(currentPlaylist[currentIndex], currentPlaylist, true);
    }
}

function nextSong() {
    if(repeat == true) {
        audioElement.setTime(0);
        playSong();
        return;
    }
    if(currentIndex == currentPlaylist.length - 1) {
        currentIndex = 0;
    } else {
        currentIndex++;
    }

    var trackToPlay = shuffle ? shufflePlaylist[currentIndex] : currentPlaylist[currentIndex];
    setTrack(trackToPlay, currentPlaylist, true);
}

function timeFromOffset(mouse, progressBar) {
    var percentage = mouse.offsetX / $(progressBar).width() * 100;
    var seconds = audioElement.audio.duration * (percentage / 100);
    audioElement.setTime(seconds);
}
