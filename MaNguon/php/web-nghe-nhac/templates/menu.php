<!DOCTYPE HTML>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <script src="https://cdn.tailwindcss.com"></script>
  <link
    rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
  />
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    body {
      font-family: 'Inter', sans-serif;
    }
    
    .nav-item {
      transition: all 0.2s ease-in-out;
      position: relative;
    }

    .nav-item:hover {
      transform: translateY(-2px);
    }

    .nav-item.active {
      color: #1db954 !important;
    }

    .nav-item.active::after {
      content: '';
      position: absolute;
      bottom: -8px;
      left: 50%;
      transform: translateX(-50%);
      width: 4px;
      height: 4px;
      background-color: #1db954;
      border-radius: 50%;
      display: none;
    }

    .nav-item:active {
      transform: scale(0.95);
    }

    @media (prefers-color-scheme: dark) {
      .bottom-nav {
        background: rgba(18, 18, 18, 0.95);
        border-color: rgba(255, 255, 255, 0.1);
      }
    }

    @layer base {
      #seek-bar::-webkit-slider-thumb {
        @apply appearance-none w-3 h-3 bg-highlight rounded-full cursor-pointer;
      }
      #volume-bar::-webkit-slider-thumb {
        @apply appearance-none w-3 h-3 bg-highlight rounded-full cursor-pointer;
      }
    }

    @layer utilities {
      .drag-bar-button:hover {
        @apply text-highlight drop-shadow-[0_0_8px_rgba(29,185,84,0.5)];
      }
      .control-buttons button:not(#main-play):hover {
        @apply text-highlight;
      }
      #main-play:hover {
        @apply bg-highlight;
      }
      .lyrics-controls button:hover {
        @apply bg-accent;
      }
      .playlist li:hover {
        @apply bg-[rgba(169,229,189,0.25)];
      }
      .lyric-line.active {
        @apply text-highlight font-bold;
      }
      .full-player {
        z-index: 1000;
        transform: translateY(100%);
      }
      .full-player.show {
        transform: translateY(0%);
      }
    }
  
   .bottom-nav {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 997;
      backdrop-filter: blur(20px);
      background: rgba(255, 255, 255, 0.95);
      box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1);
      z-index: 997;
      transition: transform 0.4s ease-in-out;
    }

    #mini-player {
      position: fixed;
      display: flex;
      align-items: center;
      justify-content: space-between;
      bottom: 80px;
      left: 50%;
      transform: translateX(-50%);
      width: 96%;
      background: rgba(255, 255, 255, 0.95);
      color: #333;
      border-radius: 12px;
      padding: 10px;
      z-index: 997;
    }

    #mini-thumb {
      width: 40px;
      height: 40px;
      border-radius: 8px;
    }

    #mini-title {
      font-size: 14px;
      font-weight: bold;
    }

    #mini-artist {
      font-size: 12px;
      color: #ccc;
    }

    #play-btn {
      font-size: 20px;
      color: #1DB954;
    }
  </style>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            'bg': '#fdfcf7',
            'panel': '#f5fff9',
            'accent': '#a9e5bd',
            'highlight': '#1DB954',
            'text': '#2c3e30',
            'text-muted': '#88a098',
            'lyrics-bg': '#eefaf3',
            'spotify-green': '#1db954',
            'spotify-black': '#191414',
            'spotify-gray': '#535353'
          },
          animation: {
            'idle-bounce': 'idle-bounce 1.8s ease-in-out infinite'
          },
          keyframes: {
            'idle-bounce': {
              '0%, 100%': { transform: 'translateY(0)' },
              '50%': { transform: 'translateY(5px)' }
            }
          }
        }
      }
    }
  </script>
</head>

<body>
  <!-- Mini Player -->
  <div id="mini-player" class="shadow-[0_-4px_12px_rgba(0,0,0,0.05)]" onclick="showFullPlayer()">
    <img id="mini-thumb" class="rounded-lg flex-shrink-0" />
    <div id="mini-info" class="ml-[3px]">
      <div id="mini-title" class="font-bold text-sm truncate">Chưa có bài hát</div>
      <div id="mini-artist" class="text-[13px] text-text-muted truncate">Chọn bài hát để bắt đầu</div>
    </div>
    <button onclick="togglePlay(event)" class="ml-auto mr-1 bg-transparent border-none text-text text-2xl" id="play-btn">
      <i class="bi bi-play-fill"></i>
    </button>
  </div>
  <!-- Full Player-->
 <div id="full-player" class="full-player fixed bottom-0 w-full h-full bg-bg transition-transform duration-400 flex flex-col">
    <div class="drag-bar-button block m-1 mx-auto bg-transparent border-none text-2xl text-text-muted cursor-pointer animate-idle-bounce" onclick="hideFullPlayer()">
      <i class="bi bi-chevron-compact-down"></i>
    </div>
    <div class="player-content p-5 overflow-y-auto flex-1">
      <img id="full-thumb" class="album-large w-full rounded-lg" />
      <h2 id="full-title" class="text-xl font-bold mt-3"></h2>
      <p id="full-artist" class="text-text-muted"></p>

      <div class="custom-controls flex items-center gap-2.5 my-3">
        <span id="current-time" class="text-sm">0:00</span>
        <input type="range" id="seek-bar" min="0" value="0" step="1" class="flex-1 h-1 bg-[#d9e9dd] rounded" />
        <span id="duration" class="text-sm">0:00</span>
      </div>

      <div class="control-buttons flex justify-center items-center gap-4 mb-3">
        <button id="shuffle-btn" class="bg-transparent border-none text-text text-xl cursor-pointer transition-colors duration-200"><i class="bi bi-shuffle"></i></button>
        <button id="prev-btn" class="bg-transparent border-none text-text text-xl cursor-pointer transition-colors duration-200"><i class="bi bi-skip-backward-fill"></i></button>
        <button id="main-play" class="bg-highlight text-white border-none w-14 h-14 text-3xl rounded-xl flex items-center justify-center transition-colors duration-300"><i class="bi bi-play-fill"></i></button>
        <button id="next-btn" class="bg-transparent border-none text-text text-xl cursor-pointer transition-colors duration-200"><i class="bi bi-skip-forward-fill"></i></button>
        <button id="loop-btn" class="bg-transparent border-none text-text text-xl cursor-pointer transition-colors duration-200"><i class="bi bi-arrow-repeat"></i></button>
      </div>

      <div class="volume-control flex items-center gap-2.5 my-3 mb-5">
        <i class="bi bi-volume-up-fill text-lg text-text"></i>
        <input type="range" id="volume-bar" min="0" max="1" step="0.01" value="1" class="flex-1 h-1 bg-[#c6e4d0] rounded" />
      </div>

      <!-- Các nút chức năng -->
      <div class="lyrics-controls flex justify-center gap-3 my-2 mb-4">
        <button id="toggle-lyrics-btn" class="py-2 px-3 bg-highlight border-none text-white rounded-md cursor-pointer text-sm transition-colors duration-200">Lời bài hát</button>
        <button id="toggle-karaoke-btn" class="py-2 px-3 bg-highlight border-none text-white rounded-md cursor-pointer text-sm transition-colors duration-200">Chế độ Karaoke</button>
      </div>

      <!-- Lời bài hát -->
      <div id="lyrics" class="lyrics-box hidden bg-lyrics-bg text-center py-5 px-2.5 whitespace-pre-wrap text-sm leading-normal rounded-lg max-h-[300px] overflow-y-auto mb-3.5 text-text"></div>

      <h3 class="playlist-title mt-6 text-base font-semibold">Danh sách bài hát</h3>
      <ul id="playlist" class="playlist list-none p-0 m-0"></ul>
    </div>

    <audio id="audio"></audio>
  </div>
  <!-- Bottom Navigation -->
  <nav id="sticky-menu" class="bottom-nav fixed bottom-0 left-0 right-0 w-full border-t border-gray-200 dark:border-gray-700">
    <ul class="flex justify-around items-center py-3 px-2 max-w-md mx-auto">
      <li>
        <a href="../index.php" class="nav-item flex flex-col items-center text-spotify-gray hover:text-gray-900 dark:hover:text-white cursor-pointer p-2 rounded-lg">
          <i class="fas fa-home text-xl mb-1"></i>
          <span class="text-xs font-medium">Home</span>
        </a>
      </li>
      <li>
        <a href="../pages/search.php" class="nav-item flex flex-col items-center text-spotify-gray hover:text-gray-900 dark:hover:text-white cursor-pointer p-2 rounded-lg">
          <i class="fas fa-search text-xl mb-1"></i>
          <span class="text-xs font-medium">Search</span>
        </a>
      </li>
      <li>
        <a href="../pages/library.php" class="nav-item flex flex-col items-center text-spotify-gray hover:text-gray-900 dark:hover:text-white cursor-pointer p-2 rounded-lg">
          <i class="fas fa-book text-xl mb-1"></i>
          <span class="text-xs font-medium">Library</span>
        </a>
      </li>
      <li>
        <a href="../pages/subscription.php" class="nav-item flex flex-col items-center text-spotify-gray hover:text-gray-900 dark:hover:text-white cursor-pointer p-2 rounded-lg">
          <i class="fas fa-crown text-xl mb-1"></i>
          <span class="text-xs font-medium">Premium</span>
        </a>
      </li>
      <li>
        <a href="../private/profile.php" class="nav-item flex flex-col items-center text-spotify-gray hover:text-gray-900 dark:hover:text-white cursor-pointer p-2 rounded-lg">
          <i class="fas fa-user text-xl mb-1"></i>
          <span class="text-xs font-medium">Profile</span>
        </a>
      </li>
    </ul>
  </nav>

  <script>
    let currentIndex = 0;
    let isLooping = false;
    let isShuffling = false;
    let karaokeMode = false;
    let isUserScrolling = false;
    let tracks = [];
    let currentTrack = null;

    const audio = document.getElementById("audio");
    const seekBar = document.getElementById("seek-bar");
    const currentTime = document.getElementById("current-time");
    const durationEl = document.getElementById("duration");
    const mainPlay = document.getElementById("main-play");
    const playBtn = document.getElementById("play-btn");
    const miniPlayer = document.getElementById("mini-player");
    const fullPlayer = document.getElementById("full-player");
    const lyricsBox = document.getElementById("lyrics");
    const playlistEl = document.getElementById("playlist");
    const prevBtn = document.getElementById("prev-btn");
    const nextBtn = document.getElementById("next-btn");
    const loopBtn = document.getElementById("loop-btn");
    const shuffleBtn = document.getElementById("shuffle-btn");
    const volumeBar = document.getElementById("volume-bar");
    const toggleLyricsBtn = document.getElementById("toggle-lyrics-btn");
    const toggleKaraokeBtn = document.getElementById("toggle-karaoke-btn");

    let lyrics = [];

    function formatTime(sec) {
      const m = Math.floor(sec / 60);
      const s = Math.floor(sec % 60);
      return `${m}:${s.toString().padStart(2, '0')}`;
    }

    // Cập nhật thanh tiến độ
    seekBar.oninput = () => {
      audio.currentTime = seekBar.value;
    };

    // Điều chỉnh âm lượng
    volumeBar.oninput = () => {
      audio.volume = volumeBar.value;
    };

    lyricsBox.addEventListener("touchstart", () => isUserScrolling = true);
    lyricsBox.addEventListener("touchend", () => {
      setTimeout(() => isUserScrolling = false, 1000);
    });

    // Cập nhật thanh tiến độ và thời gian hiện tại khi bài hát đang chạy
    audio.ontimeupdate = () => {
      if (!isUserScrolling) {
        seekBar.value = audio.currentTime;  
        currentTime.innerText = formatTime(audio.currentTime);
      }

      // Hiển thị lời bài hát
      const current = audio.currentTime;
      const lines = lyricsBox.querySelectorAll(".lyric-line");

      for (let i = 0; i < lyrics.length; i++) {
        const line = lyrics[i];
        const next = lyrics[i + 1];
        const isActive = current >= line.time && (!next || current < next.time);
        lines[i]?.classList.toggle("active", isActive);
      }

      // Cuộn lời bài hát
      const active = lyricsBox.querySelector(".lyric-line.active");
      if (active && !isUserScrolling) {
        active.scrollIntoView({
          behavior: "smooth",
          block: "center"
        });
      }
    };

    // Khi bài hát được tải và metadata được load
    audio.onloadedmetadata = () => {
      seekBar.max = audio.duration;
      durationEl.innerText = formatTime(audio.duration);
    };

    // Cập nhật biểu tượng play/pause
    audio.onplay = updatePlayIcons;
    audio.onpause = updatePlayIcons;

    // Hàm play/pause
    function togglePlay(e) {
      e?.stopPropagation();
      if (!currentTrack) return;
      audio.paused ? audio.play() : audio.pause();
    }

    // Cập nhật biểu tượng play/pause
    function updatePlayIcons() {
      const icon = audio.paused ? `<i class="bi bi-play-fill"></i>` : `<i class="bi bi-pause-fill"></i>`;
      playBtn.innerHTML = icon;
      mainPlay.innerHTML = icon;
    }

    // Chuyển bài trước
    prevBtn.onclick = () => {
      if (tracks.length === 0) return;
      currentIndex = (currentIndex - 1 + tracks.length) % tracks.length;
      loadTrack(tracks[currentIndex]);
    };

    // Chuyển bài tiếp theo
    nextBtn.onclick = () => {
      if (tracks.length === 0) return;
      isShuffling ? shuffleTrack() : loadTrack(tracks[(currentIndex + 1) % tracks.length]);
    };

    // Khi bài hát kết thúc
    audio.onended = () => {
      if (tracks.length === 0) return;
      if (isLooping) {
        loadTrack(tracks[currentIndex]);
      } else if (isShuffling) {
        shuffleTrack();
      } else {
        loadTrack(tracks[(currentIndex + 1) % tracks.length]);
      }
    };

    // Chế độ loop
    loopBtn.onclick = () => {
      isLooping = !isLooping;
      isShuffling = false;
      loopBtn.style.color = isLooping ? "#1db954" : "inherit";
      shuffleBtn.style.color = "inherit";
    };

    // Chế độ shuffle
    shuffleBtn.onclick = () => {
      isShuffling = !isShuffling;
      isLooping = false;
      shuffleBtn.style.color = isShuffling ? "#1db954" : "inherit";
      loopBtn.style.color = "inherit";
    };

    // Hiển thị/ẩn lời bài hát
    toggleLyricsBtn.onclick = () => {
      lyricsBox.classList.toggle("hidden");
    };

    // Chế độ karaoke
    toggleKaraokeBtn.onclick = () => {
      if (!currentTrack) return;
      karaokeMode = !karaokeMode;
      toggleKaraoke();
    };

    function toggleKaraoke() {
      if (karaokeMode) {
        toggleKaraokeBtn.innerText = "Tắt Karaoke";
      } else {
        toggleKaraokeBtn.innerText = "Chế độ Karaoke";
      }
    }

    function parseLRC(text) {
      lyrics = [];
      const lines = text.split("\n");
      for (const line of lines) {
        const match = line.match(/\[(\d+):(\d+\.\d+)\](.*)/);
        if (match) {
          const min = parseInt(match[1]);
          const sec = parseFloat(match[2]);
          const time = min * 60 + sec;
          const content = match[3].trim();
          lyrics.push({ time, content });
        }
      }
    }

    function renderLyrics() {
      lyricsBox.innerHTML = "";
      lyrics.forEach((line) => {
        const div = document.createElement("div");
        div.className = "lyric-line text-text-muted py-1 transition-colors transition-font duration-300";
        div.innerText = line.content;
        lyricsBox.appendChild(div);
      });
    }

    function loadTrack(track) {
      currentTrack = track;
      currentIndex = tracks.findIndex(t => t.id === track.id);
      karaokeMode = false;
      toggleKaraokeBtn.innerText = "Chế độ Karaoke";
      lyricsBox.classList.remove("hidden");

      document.getElementById("mini-thumb").src = track.artwork;
      document.getElementById("mini-title").innerText = track.name;
      document.getElementById("mini-artist").innerText = track.artist;

      document.getElementById("full-thumb").src = track.artwork;
      document.getElementById("full-title").innerText = track.name;
      document.getElementById("full-artist").innerText = track.artist;

      audio.src = track.path;
      audio.load();
      audio.play();

      if (track.lyric) {
        fetch(track.lyric)
          .then((res) => res.text())
          .then((text) => {
            parseLRC(text);
            renderLyrics();
          })
          .catch(() => {
            lyricsBox.innerHTML = "<i>Không tải được lời bài hát.</i>";
          });
      } else {
        lyricsBox.innerHTML = "<i>Không có lời bài hát.</i>";
      }

      highlightCurrentInPlaylist();
    }

    function shuffleTrack() {
      let i;
      do {
        i = Math.floor(Math.random() * tracks.length);
      } while (i === currentIndex);
      loadTrack(tracks[i]);
    }

    function highlightCurrentInPlaylist() {
      const items = document.querySelectorAll(".playlist li");
      items.forEach((li, i) => {
        li.classList.toggle("active", i === currentIndex);
      });
    }

    function initPlaylist() {
      playlistEl.innerHTML = "";
      tracks.forEach((track, i) => {
        const li = document.createElement("li");
        li.className = "py-2.5 px-3 border-b border-b-gray-200 cursor-pointer text-text";
        li.innerText = `${track.name} – ${track.artist}`;
        li.onclick = () => loadTrack(track);
        playlistEl.appendChild(li);
      });
    }

    function showFullPlayer() {
      fullPlayer.classList.add("show");
    }
    
    function hideFullPlayer() {
      fullPlayer.classList.remove("show");
    }

    // Xử lý sự kiện khi bài hát được chọn từ song.php
    window.addEventListener('songSelected', (e) => {
      const song = e.detail;
      
      // Kiểm tra xem bài hát đã có trong tracks chưa
      const existingIndex = tracks.findIndex(t => t.id === song.id);
      
      if (existingIndex === -1) {
        // Thêm bài hát mới vào danh sách
        tracks = [song];
        currentIndex = 0;
      } else {
        currentIndex = existingIndex;
      }
      
      // Tải bài hát
      loadTrack(song);
      
      // Cập nhật playlist
      initPlaylist();
    });

    window.onload = () => {
      updatePlayIcons();
      mainPlay.onclick = (e) => togglePlay(e);
    };
  </script>
</body>
</html>