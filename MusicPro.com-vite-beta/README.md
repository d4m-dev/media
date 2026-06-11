# Music Pro Ultimate - React Version

A modern music player application built with React and Vite, featuring a responsive layout that works perfectly on all screen sizes including 16-inch displays.

## Project Structure

```
src/
├── components/           # Reusable UI components
│   ├── TrackList.jsx     # Track listing component
│   ├── MiniPlayer.jsx    # Mini player component
│   └── FullPlayer.jsx    # Full player component
├── pages/               # Page components
│   ├── TrangChu.jsx     # Home page
│   ├── KhamPha.jsx      # Explore page
│   ├── YeuThich.jsx     # Favorites page
│   └── CaiDat.jsx       # Settings page
├── assets/              # Static assets (images, fonts, etc.)
├── utils/               # Utility functions
│   └── dataService.js   # Data loading and management
├── contexts/            # React context providers
│   └── MusicContext.jsx # Global music state management
├── App.jsx              # Main application component
├── main.jsx             # Application entry point
├── styles.css           # Global styles
├── tracks.js            # Song data
└── playlists.js         # Playlist data
```

## Features

- **Responsive Layout**: Adapts to different screen sizes (1 column on mobile, 2 on tablet, 3 on desktop)
- **Multi-page Interface**: Separate pages for home, explore, favorites, and settings
- **Full Music Player**: With playback controls, volume, progress bar, etc.
- **Theme Support**: Light and dark themes
- **Favorites System**: Ability to mark songs as favorites
- **Search Functionality**: Search through tracks
- **Data Integration**: Gets song data from tracks.js and playlist data from playlists.js
- **Explore Page**: Shows data from playlists.js (remix, tet, lofi playlists)

## Installation

```bash
npm install
```

## Development

```bash
npm run dev
```

## Build

```bash
npm run build
```

## Troubleshooting

If you encounter errors during installation, try these solutions:

### Cache Issues
If you get errors related to npm cache or corrupted packages:
```bash
npm cache clean --force
npm install
```

### Network Issues
If you get network-related errors:
```bash
npm config set registry https://registry.npmjs.org/
npm install
```

### Permission Issues
If you get permission errors:
```bash
sudo chown -R $(whoami) ~/.npm
npm install
```

## Pages

- **TrangChu (Home)**: Main track listing with search and filtering
- **KhamPha (Explore)**: Discovery page with recommendations from playlists.js
- **YeuThich (Favorites)**: List of favorite tracks
- **CaiDat (Settings)**: Application settings and preferences

## Data Sources

- **tracks.js**: Contains all song information (title, artist, artwork, audio files, etc.)
- **playlists.js**: Contains curated playlists (remix, tet, lofi, etc.)
- **dataService.js**: Handles loading and normalization of track and playlist data
- **MusicContext.jsx**: Manages global state for tracks, playlists, favorites, and current playback

## Components

- **TrackList**: Displays tracks in a responsive grid
- **MiniPlayer**: Compact player that stays at the bottom
- **FullPlayer**: Detailed player with all controls