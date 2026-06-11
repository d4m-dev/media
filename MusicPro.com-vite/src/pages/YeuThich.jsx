import React, { useState, useEffect } from 'react';
import { useMusic } from '../../contexts/MusicContext.jsx';
import TrackList from '../components/TrackList.jsx';

const YeuThich = () => {
  const { tracks, searchQuery, setSearchQuery, favorites, toggleFavorite } = useMusic();

  // Filter tracks to show only favorites
  const favoriteTracks = tracks.filter(track => favorites.includes(track.id));

  const filteredTracks = favoriteTracks.filter(track => {
    return track.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
           track.artist.toLowerCase().includes(searchQuery.toLowerCase());
  });

  return (
    <div className="page-container">
      <div className="search-wrapper">
        <div className="search-box">
          <i className="fa-solid fa-magnifying-glass"></i>
          <input 
            type="text" 
            id="search-input" 
            placeholder="Tìm tên bài hát, ca sĩ..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          {searchQuery && (
            <button id="btn-clear-search" onClick={() => setSearchQuery('')}>
              <i className="fa-solid fa-xmark"></i>
            </button>
          )}
        </div>
      </div>

      <div className="list-container" id="main-scroll">
        <div className="list-header">
          <div className="header-main">
            <h2>Bài hát yêu thích</h2>
            <p>{favoriteTracks.length} bài hát • Cập nhật gần đây</p>
          </div>
        </div>
        
        <TrackList 
          tracks={filteredTracks} 
          onToggleFavorite={toggleFavorite}
        />
        <div style={{ height: '150px' }}></div>
      </div>
    </div>
  );
};

export default YeuThich;