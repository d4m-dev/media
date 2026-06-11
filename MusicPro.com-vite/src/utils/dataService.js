// Data service to handle tracks, playlists, and favorites
import { TRACKS as LocalTracks } from './tracks.js';

const TRACKS_URL = './tracks.js';

const normalizeTracks = (items = []) => items.map((item) => ({
    id: item.id,
    name: item.title || item.name || 'Tạm thời chưa có!',
    artist: item.artist || 'Tạm thời chưa có!',
    artwork: item.cover || item.artwork || 'Tạm thời chưa có!',
    path: item.audioSrc || item.path || 'Tạp thời chưa có!',
    instrumental: item.instrumentalSrc || item.instrumental || 'Tạm thời chưa có!',
    vid: item.videoSrc || item.vid || 'Tạm thời chưa có!',
    lyric: item.lyricSrc || item.lyric || 'Tạm thời chưa có!'
}));

export const loadTracks = async () => {
    // Ưu tiên sử dụng tracks import từ local nếu có
    if (Array.isArray(LocalTracks) && LocalTracks.length) return LocalTracks;

    // Fallback: Logic cũ nếu muốn load từ remote (giữ nguyên để tương thích)
    if (Array.isArray(window.TRACKS) && window.TRACKS.length) return window.TRACKS;
    try {
        const res = await fetch(TRACKS_URL, { cache: 'force-cache' });
        const text = await res.text();
        const sandbox = {};
        const getter = new Function('window', `${text}; return window.TRACKS || [];`);
        const data = getter(sandbox);
        return Array.isArray(data) ? data : [];
    } catch (e) { 
        console.error('Error loading tracks:', e);
        return []; 
    }
};

export const loadPlaylists = async () => {
    try {
        const res = await fetch('./playlists.js');
        if (res.ok) {
            const text = await res.text();
            // Evaluate the playlists data
            const playlists = {};
            eval(text); // This will populate the global PLAYLIST_* variables
            return {
                remix: window.PLAYLIST_REMIX || [],
                tet: window.PLAYLIST_TET || [],
                lofi: window.PLAYLIST_LOFI || []
            };
        }
    } catch (e) {
        console.error('Error loading playlists:', e);
        return { remix: [], tet: [], lofi: [] };
    }
};

export const getFavorites = () => {
    return JSON.parse(localStorage.getItem('favorites') || '[]');
};

export const toggleFavorite = (trackId) => {
    const favorites = getFavorites();
    const newFavorites = favorites.includes(trackId)
        ? favorites.filter(id => id !== trackId)
        : [...favorites, trackId];
    
    localStorage.setItem('favorites', JSON.stringify(newFavorites));
    return newFavorites;
};