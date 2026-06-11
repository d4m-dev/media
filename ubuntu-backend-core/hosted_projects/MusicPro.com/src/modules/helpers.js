const TRACKS_URL = 'src/tracks.js';

const normalizeTracks = (items = []) => items.map((item) => ({
    id: item.id,
    name: item.title || item.name || '',
    artist: item.artist || '',
    artwork: item.cover || item.artwork || '',
    path: item.audioSrc || item.path || '',
    instrumental: item.instrumentalSrc || item.instrumental || '',
    vid: item.videoSrc || item.vid || '',
    lyric: item.lyricSrc || item.lyric || ''
}));

const loadRemoteTracks = async () => {
    if (Array.isArray(window.TRACKS) && window.TRACKS.length) return window.TRACKS;
    try {
        const res = await fetch(TRACKS_URL + '?v=' + Date.now(), { cache: 'no-cache' });
        if (res.ok) {
            const text = await res.text();
            const sandbox = {};
            const getter = new Function('window', `${text}; return window.TRACKS || [];`);
            return getter(sandbox) || [];
        }
    } catch (e) { console.log('Lấy dữ liệu từ xa không thành công, thử cục bộ...'); }

    try {
        const res = await fetch('src/tracks.js');
        if (res.ok) {
            const text = await res.text();
            const sandbox = {};
            const getter = new Function('window', `${text}; return window.TRACKS || [];`);
            return getter(sandbox) || [];
        }
    } catch (e) { console.error('lỗi khi lấy dữ liệu track', e); }
    return [];
};

window.MusicProModules = window.MusicProModules || {};
window.MusicProModules.helpers = { TRACKS_URL, normalizeTracks, loadRemoteTracks };
