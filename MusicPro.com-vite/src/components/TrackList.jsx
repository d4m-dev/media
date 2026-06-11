import React, { useState, useEffect } from 'react';
import { useMusic } from '../../contexts/MusicContext.jsx';

const TrackList = ({ tracks, onPlay, onToggleFavorite }) => {
  const { favorites } = useMusic();

  const handlePlay = (track) => {
    if (onPlay) {
      onPlay(track);
    }
  };

  // Calculate rows for responsive grid
  const width = typeof window !== 'undefined' ? window.innerWidth : 1024;
  let itemsPerRow = 1;
  if (width >= 1024) {
    itemsPerRow = 3;
  } else if (width >= 768) {
    itemsPerRow = 2;
  }

  // Group tracks into rows for grid layout
  const groupedTracks = [];
  for (let i = 0; i < tracks.length; i += itemsPerRow) {
    groupedTracks.push(tracks.slice(i, i + itemsPerRow));
  }

  return (
    <div id="track-list" style={{ display: 'grid', gridTemplateColumns: `repeat(${itemsPerRow}, 1fr)`, gap: '16px' }}>
      {tracks.map((track, index) => {
        const isFav = favorites.includes(track.id);
        return (
          <div 
            key={track.id} 
            className={`track-item ${track.active ? 'active' : ''}`}
            onClick={() => handlePlay(track)}
          >
            <div className="track-thumb">
              <img src={track.artwork} loading="lazy" alt={track.name} />
              <div className="wave-anim">
                <div className="bar"></div>
                <div className="bar"></div>
                <div className="bar"></div>
              </div>
            </div>
            <div className="track-info">
              <div className="track-title">{track.name}</div>
              <div className="track-artist">{track.artist}</div>
            </div>
            <div style={{ display: 'flex', gap: '5px' }}>
              <button 
                className={`btn-icon btn-favorite-sm ${isFav ? 'active' : ''}`} 
                onClick={(e) => {
                  e.stopPropagation();
                  if (onToggleFavorite) {
                    onToggleFavorite(track.id);
                  }
                }}
              >
                <i className={`fa-${isFav ? 'solid' : 'regular'} fa-heart`}></i>
              </button>
              <button 
                className="btn-icon btn-download-sm"
                onClick={(e) => {
                  e.stopPropagation();
                  // Handle download
                }}
              >
                <i className="fa-solid fa-download"></i>
              </button>
              <button 
                className="btn-icon btn-more-sm"
                onClick={(e) => {
                  e.stopPropagation();
                  // Handle more options
                }}
              >
                <i className="fa-solid fa-ellipsis"></i>
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default TrackList;