# MusicPro.com Python Edition

🎵 Music streaming application built with Python Flask - Same interface and functionality as MusicPro.com

## Features

- 🎵 Stream music tracks
- 🔍 Search songs and artists
- ❤️ Favorite tracks
- 🎼 Lyrics display
- 📹 Video playback
- 🌙 Dark/Light theme
- ⏱️ Sleep timer
- 🎚️ Equalizer controls
- 📱 Responsive design

## Project Structure

```
MusicPro.com-python/
├── app.py              # Flask backend server
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── templates/         # HTML templates
│   └── index.html     # Main page template
├── static/           # Static files
│   ├── css/         # Stylesheets
│   │   └── styles.css
│   ├── js/          # JavaScript files
│   │   ├── tracks.js
│   │   └── app.js
│   └── favicon/     # Favicon files
└── data/            # User data (auto-created)
    ├── favorites.json
    ├── history.json
    ├── settings.json
    └── playlists.json
```

## Installation

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the application

**Option 1: Run from public folder (Recommended)**

```bash
cd public
python index.py
```

**Option 2: Run from root folder**

```bash
python app.py
```

### 3. Open in browser

Navigate to: `http://localhost:5000`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main page |
| `/api/tracks` | GET | Get all tracks |
| `/api/tracks/<id>` | GET | Get track by ID |
| `/api/search?q=<query>` | GET | Search tracks |
| `/api/favorites` | GET/POST | Manage favorites |
| `/api/history` | GET/POST | Manage history |
| `/api/settings` | GET/POST | Manage settings |
| `/api/playlist` | GET/POST | Manage playlists |

## Requirements

- Python 3.8+
- Flask 3.0.0

## License

MIT License

## Credits

Original MusicPro.com project
