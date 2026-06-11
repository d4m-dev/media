import React from 'react';

const MiniPlayer = ({ currentSong, isPlaying, onPlayClick }) => {
  if (!currentSong) {
    return null;
  }

  return (
    <div className={`mini-player ${isPlaying ? '' : 'hide'}`}>
      <div className="progress-line">
        <div className="progress-fill" id="mini-fill" style={{ width: '30%' }}></div>
      </div>
      <div className="mini-content" id="mini-click-area" onClick={onPlayClick}>
        <div className="mini-img-box">
          <img id="mini-img" src={currentSong.artwork} alt={currentSong.name} />
        </div>
        <div className="mini-text-box">
          <span className="mini-title" id="mini-title">{currentSong.name}</span>
          <span className="mini-status" id="mini-artist">{currentSong.artist}</span>
        </div>
        <div className="flex-center" style={{ gap: '5px' }}>
          <button className="btn-icon" id="btn-mini-play" onClick={(e) => { e.stopPropagation(); }}>
            <i className={`fa-solid ${isPlaying ? 'fa-pause' : 'fa-play'}`}></i>
          </button>
          <button className="btn-icon" id="btn-mini-next" onClick={(e) => e.stopPropagation()}>
            <i className="fa-solid fa-forward-step"></i>
          </button>
        </div>
      </div>
    </div>
  );
};

export default MiniPlayer;