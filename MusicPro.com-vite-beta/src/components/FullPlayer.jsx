import React, { useState, useEffect } from 'react';

const FullPlayer = ({ song, isPlaying, onPlayPause, onClose, tracks, currentTrackIndex }) => {
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(240); // 4 minutes default
  const [volume, setVolume] = useState(0.8);
  const [currentMode, setCurrentMode] = useState('song'); // song, video, lyrics
  const [isMuted, setIsMuted] = useState(false);
  const [isShuffle, setIsShuffle] = useState(false);
  const [repeatMode, setRepeatMode] = useState(0); // 0: no repeat, 1: repeat one, 2: repeat all

  // Simulate progress
  useEffect(() => {
    let interval = null;
    if (isPlaying) {
      interval = setInterval(() => {
        setCurrentTime(prev => {
          if (prev >= duration) {
            onPlayPause(); // Pause when song ends
            return 0;
          }
          return prev + 1;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isPlaying, duration, onPlayPause]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  const handleNext = () => {
    const nextIndex = (currentTrackIndex + 1) % tracks.length;
    // In a real app, this would update the current song
  };

  const handlePrev = () => {
    const prevIndex = (currentTrackIndex - 1 + tracks.length) % tracks.length;
    // In a real app, this would update the current song
  };

  const handleSeek = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const pos = (e.clientX - rect.left) / rect.width;
    setCurrentTime(pos * duration);
  };

  const handleVolumeChange = (e) => {
    const vol = parseFloat(e.target.value);
    setVolume(vol);
    setIsMuted(vol === 0);
  };

  const toggleMute = () => {
    setIsMuted(!isMuted);
    if (isMuted) {
      setVolume(0.8); // restore previous volume
    } else {
      setVolume(0);
    }
  };

  return (
    <div className="player-overlay" id="player-overlay">
      <div className="ambient-glow" id="ambient-light" style={{ background: 'radial-gradient(circle, hsl(240,70%,50%), transparent 70%)' }}></div>
      <div className="overlay-header">
        <button className="btn-icon" id="btn-close" onClick={onClose}>
          <i className="fa-solid fa-chevron-down"></i>
        </button>
        <div className="tab-switcher">
          <div 
            className={`tab-btn ${currentMode === 'song' ? 'active' : ''}`} 
            data-tab="song"
            onClick={() => setCurrentMode('song')}
          >
            SONG
          </div>
          <div 
            className={`tab-btn ${currentMode === 'video' ? 'active' : ''}`} 
            data-tab="video"
            onClick={() => setCurrentMode('video')}
          >
            VIDEO
          </div>
          <div 
            className={`tab-btn ${currentMode === 'lyrics' ? 'active' : ''}`} 
            data-tab="lyrics"
            onClick={() => setCurrentMode('lyrics')}
          >
            LYRICS
          </div>
        </div>
        <div style={{ position: 'relative' }}>
          <button className="btn-icon" id="btn-options">
            <i className="fa-solid fa-ellipsis-vertical"></i>
          </button>
          <div className="options-menu" id="options-menu">
            <div className="menu-item" id="btn-switch-beat">
              <i className="fa-solid fa-microphone-lines"></i>
              <span>Chuyển sang Beat</span>
              <div className="toggle-switch"></div>
            </div>
            <div className="menu-item" id="btn-open-timer">
              <i className="fa-regular fa-clock"></i>
              <span id="timer-menu-text">Hẹn giờ tắt</span>
            </div>
          </div>
        </div>
      </div>

      <div className="player-stage">
        <div className={`stage-view ${currentMode === 'song' ? 'active' : ''}`} id="view-song">
          <div className="artwork-card">
            <img id="full-artwork" src={song.artwork} alt={song.name} />
          </div>
        </div>
        <div className={`stage-view ${currentMode === 'video' ? 'active' : ''}`} id="view-video">
          <div className="video-container">
            <video id="video-element" playsInline webkit-playsinline controls style={{ width: '100%', height: 'auto' }}>
              <source src={song.path} type="audio/mpeg" />
            </video>
            <div className="video-fallback" id="video-msg" style={{ display: 'none' }}>
              <div className="loader-ring" style={{ width: '30px', height: '30px', borderWidth: '3px' }}></div>
              <span>Đang tải Video...</span>
            </div>
          </div>
        </div>
        <div className={`stage-view ${currentMode === 'lyrics' ? 'active' : ''}`} id="view-lyrics">
          <div className="lyrics-container" id="lyrics-content">
            <p style={{ textAlign: 'center', color: 'var(--text-sub)' }}>Chức năng đang phát triển...</p>
          </div>
        </div>
      </div>

      <div className="player-controls">
        <div className="meta-info">
          <div className="song-texts">
            <div className="marquee-wrapper" id="marquee-box-title">
              <span className="marquee-content text-h1" id="full-title">{song.name}</span>
            </div>
            <div className="marquee-wrapper" id="marquee-box-artist">
              <span className="marquee-content text-h2" id="full-artist">{song.artist}</span>
            </div>
          </div>
          <div className="flex-center" style={{ gap: '10px' }}>
            <button className="btn-icon" id="btn-dl">
              <i className="fa-solid fa-download"></i>
            </button>
            <button className="btn-icon" id="btn-heart">
              <i className="fa-regular fa-heart"></i>
            </button>
          </div>
        </div>

        <div className="slider-group">
          <div className="progress-container" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span id="curr-time" style={{ fontSize: '12px', color: 'var(--text-sub)', width: '40px' }}>
              {formatTime(currentTime)}
            </span>
            <input 
              type="range" 
              id="seek-bar" 
              value={duration ? (currentTime / duration) * 100 : 0} 
              min="0" 
              max="100" 
              step="0.1"
              onChange={handleSeek}
              style={{ flex: 1 }}
            />
            <span id="total-time" style={{ fontSize: '12px', color: 'var(--text-sub)', width: '40px' }}>
              {formatTime(duration)}
            </span>
          </div>
        </div>

        <div className="controls-row">
          <button 
            className={`btn-icon ${isShuffle ? 'active' : ''}`} 
            id="btn-shuffle"
            onClick={() => setIsShuffle(!isShuffle)}
          >
            <i className="fa-solid fa-shuffle"></i>
          </button>
          <button className="btn-icon" id="btn-prev" style={{ fontSize: '24px' }} onClick={handlePrev}>
            <i className="fa-solid fa-backward-step"></i>
          </button>
          <button 
            className="btn-play-xl" 
            id="btn-main-play" 
            onClick={onPlayPause}
          >
            <i className={`fa-solid ${isPlaying ? 'fa-pause' : 'fa-play'}`}></i>
          </button>
          <button className="btn-icon" id="btn-next" style={{ fontSize: '24px' }} onClick={handleNext}>
            <i className="fa-solid fa-forward-step"></i>
          </button>
          <button 
            className={`btn-icon ${repeatMode ? 'active' : ''}`} 
            id="btn-repeat"
            onClick={() => setRepeatMode(repeatMode === 2 ? 0 : repeatMode + 1)}
          >
            <i className={`fa-solid fa-repeat ${repeatMode === 1 ? 'repeat-one' : ''}`}></i>
          </button>
        </div>

        <div className="vol-wrapper">
          <button className="btn-icon" id="btn-mute" style={{ width: '30px', height: '30px', fontSize: '16px' }} onClick={toggleMute}>
            <i className={`fa-solid fa-volume-${isMuted ? 'xmark' : 'high'}`}></i>
          </button>
          <input 
            type="range" 
            id="vol-bar" 
            min="0" 
            max="1" 
            step="0.05" 
            value={isMuted ? 0 : volume}
            onChange={handleVolumeChange}
          />
        </div>
      </div>
    </div>
  );
};

export default FullPlayer;