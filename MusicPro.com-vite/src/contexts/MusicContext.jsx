import React, { createContext, useContext, useState, useEffect } from 'react';
import { loadTracks, loadPlaylists, getFavorites, toggleFavorite } from '../utils/dataService';

const MusicContext = createContext();

export const MusicProvider = ({ children }) => {
  const [tracks, setTracks] = useState([]);
  const [playlists, setPlaylists] = useState({ remix: [], tet: [], lofi: [] });
  const [favorites, setFavorites] = useState([]);
  const [currentSong, setCurrentSong] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [currentFilter, setCurrentFilter] = useState('all');
  const [sortBy, setSortBy] = useState('id');
  const [theme, setTheme] = useState('dark');

  useEffect(() => {
    const fetchData = async () => {
      const loadedTracks = await loadTracks();
      const normalizedTracks = loadedTracks.map((item, index) => ({
        id: item.id || index,
        name: item.title || item.name || 'Tạm thời chưa có!',
        artist: item.artist || 'Tạm thời chưa có!',
        artwork: item.cover || item.artwork || 'https://placehold.co/300x300',
        path: item.audioSrc || item.path || '',
        instrumental: item.instrumentalSrc || item.instrumental || '',
        vid: item.videoSrc || item.vid || '',
        lyric: item.lyricSrc || item.lyric || '',
        favorite: false
      }));
      
      setTracks(normalizedTracks);
      setFavorites(getFavorites());
      
      const loadedPlaylists = await loadPlaylists();
      setPlaylists(loadedPlaylists);
    };

    fetchData();
  }, []);

  const toggleFavoriteHandler = (trackId) => {
    const newFavorites = toggleFavorite(trackId);
    setFavorites(newFavorites);
    
    // Update the track's favorite status in the tracks list
    setTracks(prevTracks => 
      prevTracks.map(track => 
        track.id === trackId ? { ...track, favorite: newFavorites.includes(trackId) } : track
      )
    );
  };

  const value = {
    tracks,
    playlists,
    favorites,
    currentSong,
    isPlaying,
    searchQuery,
    currentFilter,
    sortBy,
    theme,
    setCurrentSong,
    setIsPlaying,
    setSearchQuery,
    setCurrentFilter,
    setSortBy,
    setTheme,
    toggleFavorite: toggleFavoriteHandler
  };

  return (
    <MusicContext.Provider value={value}>
      {children}
    </MusicContext.Provider>
  );
};

export const useMusic = () => {
  const context = useContext(MusicContext);
  if (!context) {
    throw new Error('useMusic must be used within a MusicProvider');
  }
  return context;
};