import React, { useState, useEffect } from 'react';
import { useMusic } from '../../contexts/MusicContext.jsx';

const KhamPha = () => {
  const { tracks, playlists, searchQuery, setSearchQuery } = useMusic();
  const [exploreSections, setExploreSections] = useState([]);
  
  useEffect(() => {
    // Create explore sections based on playlists data
    const sections = [];
    
    // Recently played (using first few tracks as example)
    if (tracks.length > 0) {
      sections.push({
        title: 'Gần đây',
        items: tracks.slice(0, 3).map(track => ({
          id: track.id,
          name: track.name,
          artist: track.artist,
          artwork: track.artwork
        }))
      });
    }
    
    // Playlist sections from playlists.js
    if (playlists.remix && playlists.remix.length > 0) {
      const remixTracks = tracks.filter(track => playlists.remix.includes(track.id));
      if (remixTracks.length > 0) {
        sections.push({
          title: 'Nhạc Remix',
          items: remixTracks.slice(0, 3).map(track => ({
            id: track.id,
            name: track.name,
            artist: track.artist,
            artwork: track.artwork
          }))
        });
      }
    }
    
    if (playlists.tet && playlists.tet.length > 0) {
      const tetTracks = tracks.filter(track => playlists.tet.includes(track.id));
      if (tetTracks.length > 0) {
        sections.push({
          title: 'Nhạc Tết',
          items: tetTracks.slice(0, 3).map(track => ({
            id: track.id,
            name: track.name,
            artist: track.artist,
            artwork: track.artwork
          }))
        });
      }
    }
    
    if (playlists.lofi && playlists.lofi.length > 0) {
      const lofiTracks = tracks.filter(track => playlists.lofi.includes(track.id));
      if (lofiTracks.length > 0) {
        sections.push({
          title: 'Lofi',
          items: lofiTracks.slice(0, 3).map(track => ({
            id: track.id,
            name: track.name,
            artist: track.artist,
            artwork: track.artwork
          }))
        });
      }
    }
    
    // Recommendations based on all tracks
    if (tracks.length > 0) {
      sections.push({
        title: 'Đề xuất cho bạn',
        items: tracks.slice(3, 6).map(track => ({
          id: track.id,
          name: track.name,
          artist: track.artist,
          artwork: track.artwork
        }))
      });
    }
    
    setExploreSections(sections);
  }, [tracks, playlists]);

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

      <div className="explore-container">
        {exploreSections.map((section, index) => (
          <div key={index} className="explore-section">
            <div className="explore-header">
              <h3 className="explore-title">{section.title}</h3>
              <button className="btn-see-all">Xem tất cả</button>
            </div>
            <div className="history-grid">
              {section.items.map(item => (
                <div key={item.id} className="history-item">
                  <img src={item.artwork} className="history-img" alt={item.name} />
                  <div className="history-title">{item.name}</div>
                  <div className="history-artist">{item.artist}</div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default KhamPha;