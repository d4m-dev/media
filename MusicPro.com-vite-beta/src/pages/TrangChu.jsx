import React, { useState, useEffect } from 'react';
import { useMusic } from '../../contexts/MusicContext.jsx';
import TrackList from '../components/TrackList.jsx';
import MiniPlayer from '../components/MiniPlayer.jsx';
import FullPlayer from '../components/FullPlayer.jsx';

const TrangChu = () => {
  const { tracks, searchQuery, currentFilter, sortBy, currentSong, isPlaying, setSearchQuery, setCurrentFilter, setSortBy, setCurrentSong, setIsPlaying, toggleFavorite } = useMusic();
  const [showPlayer, setShowPlayer] = useState(false);

  const filters = [
    { type: 'all', label: 'Tất Cả' },
    { type: 'remix', label: 'Nhạc Remix' },
    { type: 'tet', label: 'Nhạc Tết' },
    { type: 'lofi', label: 'Lofi' },
    { type: 'favorites', label: 'Yêu thích' }
  ];

  // Filter tracks based on current filter and search query
  const filteredTracks = tracks.filter(track => {
    let matchesFilter = true;
    
    if (currentFilter === 'favorites') {
      matchesFilter = track.favorite || false;
    } else if (currentFilter !== 'all') {
      // For other filters, we'd need to check against playlists
      // For now, we'll just show all tracks for non-favorites filters
      matchesFilter = true;
    }
    
    const matchesSearch = track.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          track.artist.toLowerCase().includes(searchQuery.toLowerCase());
    
    return matchesFilter && matchesSearch;
  });

  // Sort tracks based on selected sort option
  const sortedTracks = [...filteredTracks].sort((a, b) => {
    if (sortBy === 'name') {
      return a.name.localeCompare(b.name, 'vi');
    } else {
      return b.id - a.id;
    }
  });

  const handlePlaySong = (song) => {
    setCurrentSong(song);
    setIsPlaying(true);
    setShowPlayer(true);
  };

  const handleToggleFavorite = (trackId) => {
    toggleFavorite(trackId);
  };

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

      <div className="chips-wrapper">
        <div className="chips-row">
          {filters.map(filter => (
            <span 
              key={filter.type}
              className={`chip ${currentFilter === filter.type ? 'active' : ''}`}
              data-type={filter.type}
              onClick={() => setCurrentFilter(filter.type)}
            >
              {filter.label}
            </span>
          ))}
        </div>
      </div>

      <div className="list-container" id="main-scroll">
        <div className="list-header">
          <div className="header-main">
            <h2>{currentFilter === 'favorites' ? 'Bài hát yêu thích' : 'Danh sách phát'}</h2>
            <p>Cập nhật hôm nay • Dành riêng cho bạn</p>
          </div>
          <div className="sort-controls" id="sort-controls" style={{ display: currentFilter === 'favorites' ? 'none' : 'flex' }}>
            <button 
              className={`btn-sort ${sortBy === 'id' ? 'active' : ''}`} 
              data-sort="id"
              onClick={() => setSortBy('id')}
            >
              <i className="fa-solid fa-clock"></i> <span>Mới nhất</span>
            </button>
            <button 
              className={`btn-sort ${sortBy === 'name' ? 'active' : ''}`} 
              data-sort="name"
              onClick={() => setSortBy('name')}
            >
              <i className="fa-solid fa-font"></i> <span>Tên A-Z</span>
            </button>
          </div>
        </div>
        
        <TrackList 
          tracks={sortedTracks} 
          onPlay={handlePlaySong} 
          onToggleFavorite={handleToggleFavorite}
        />
        <div style={{ height: '150px' }}></div>
      </div>

      <MiniPlayer currentSong={currentSong} isPlaying={isPlaying} onPlayClick={() => setShowPlayer(true)} />
      
      {showPlayer && currentSong && (
        <FullPlayer 
          song={currentSong} 
          isPlaying={isPlaying}
          onClose={() => setShowPlayer(false)} 
          onPlayPause={() => setIsPlaying(!isPlaying)}
          tracks={tracks}
          currentTrackIndex={tracks.findIndex(t => t.id === currentSong?.id)}
        />
      )}
    </div>
  );
};

export default TrangChu;