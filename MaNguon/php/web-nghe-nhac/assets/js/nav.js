let currentIndex = 0;
let isLooping = false;
let isShuffling = false;
let karaokeMode = false;
let isUserScrolling = false;

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

seekBar.oninput = () => {
  audio.currentTime = seekBar.value;
};

volumeBar.oninput = () => {
  audio.volume = volumeBar.value;
};

lyricsBox.addEventListener("touchstart", () => isUserScrolling = true);
lyricsBox.addEventListener("touchend", () => {
  setTimeout(() => isUserScrolling = false, 1000);
});

audio.ontimeupdate = () => {
  seekBar.value = audio.currentTime;
  currentTime.innerText = formatTime(audio.currentTime);

  const current = audio.currentTime;
  const lines = lyricsBox.querySelectorAll(".lyric-line");

  for (let i = 0; i < lyrics.length; i++) {
    const line = lyrics[i];
    const next = lyrics[i + 1];
    const isActive = current >= line.time && (!next || current < next.time);
    lines[i]?.classList.toggle("active", isActive);
  }

  const active = lyricsBox.querySelector(".lyric-line.active");
  if (active && !isUserScrolling) {
    active.scrollIntoView({
      behavior: "smooth",
      block: "center"
    });
  }
};

audio.onloadedmetadata = () => {
  seekBar.max = audio.duration;
  durationEl.innerText = formatTime(audio.duration);
};

audio.onplay = updatePlayIcons;
audio.onpause = updatePlayIcons;

function togglePlay(e) {
  e?.stopPropagation();
  audio.paused ? audio.play() : audio.pause();
}

function updatePlayIcons() {
  const icon = audio.paused ? `<i class="bi bi-play-fill"></i>` : `<i class="bi bi-pause-fill"></i>`;
  playBtn.innerHTML = icon;
  mainPlay.innerHTML = icon;
}

prevBtn.onclick = () => {
  currentIndex = (currentIndex - 1 + tracks.length) % tracks.length;
  loadTrack(currentIndex);
};

nextBtn.onclick = () => {
  isShuffling ? shuffleTrack() : loadTrack((currentIndex + 1) % tracks.length);
};

audio.onended = () => {
  if (isLooping) {
    loadTrack(currentIndex);
  } else if (isShuffling) {
    shuffleTrack();
  } else {
    loadTrack((currentIndex + 1) % tracks.length);
  }
};

loopBtn.onclick = () => {
  isLooping = !isLooping;
  isShuffling = false;
  loopBtn.style.color = isLooping ? "#1db954" : "inherit";
  shuffleBtn.style.color = "inherit";
};

shuffleBtn.onclick = () => {
  isShuffling = !isShuffling;
  isLooping = false;
  shuffleBtn.style.color = isShuffling ? "#1db954" : "inherit";
  loopBtn.style.color = "inherit";
};

toggleLyricsBtn.onclick = () => {
  lyricsBox.classList.toggle("hidden");
};

toggleKaraokeBtn.onclick = () => {
  karaokeMode = !karaokeMode;
  toggleKaraoke();
};

function toggleKaraoke() {
  const track = tracks[currentIndex];
  if (karaokeMode) {
    if (track.instrumental) {
      audio.src = track.instrumental;
      toggleKaraokeBtn.innerText = "Tắt Karaoke";
    } else {
      alert("Hiện chưa có bản không lời");
      karaokeMode = false;
      toggleKaraokeBtn.innerText = "Chế độ Karaoke";
      return;
    }
  } else {
    audio.src = track.path;
    toggleKaraokeBtn.innerText = "Chế độ Karaoke";
  }

  audio.load();
  audio.play();
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
    div.className = "lyric-line";
    div.innerText = line.content;
    lyricsBox.appendChild(div);
  });
}

function loadTrack(index) {
  const track = tracks[index];
  currentIndex = index;
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

  miniPlayer.classList.add("show");

  fetch(track.lyric)
    .then((res) => res.text())
    .then((text) => {
      parseLRC(text);
      renderLyrics();
    })
    .catch(() => {
      lyricsBox.innerHTML = "<i>Không tải được lời bài hát.</i>";
    });

  highlightCurrentInPlaylist();
}

function shuffleTrack() {
  let i;
  do {
    i = Math.floor(Math.random() * tracks.length);
  } while (i === currentIndex);
  loadTrack(i);
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
    li.innerText = `${track.name} – ${track.artist}`;
    li.onclick = () => loadTrack(i);
    playlistEl.appendChild(li);
  });
}

function showFullPlayer() {
  fullPlayer.classList.add("show");
}
function hideFullPlayer() {
  fullPlayer.classList.remove("show");
}

window.onload = () => {
  initPlaylist();
  loadTrack(0);
  updatePlayIcons();
  mainPlay.onclick = (e) => togglePlay(e);
};
function toggleKaraoke() {
  const track = tracks[currentIndex];
  const currentTime = audio.currentTime;
  const wasPlaying = !audio.paused;

  const newSrc = karaokeMode
    ? track.instrumental
    : track.path;

  if (karaokeMode && !track.instrumental) {
    alert("Hiện chưa có bản không lời");
    karaokeMode = false;
    toggleKaraokeBtn.innerText = "Chế độ Karaoke";
    return;
  }

  audio.src = newSrc;
  audio.load();

  audio.onloadedmetadata = () => {
    if (wasPlaying) audio.play();
  };

  toggleKaraokeBtn.innerText = karaokeMode ? "Tắt Karaoke" : "Chế độ Karaoke";
}