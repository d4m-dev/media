#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MusicPro.com Python Version
Flask-based music streaming application
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import os
import re

app = Flask(__name__)


def load_tracks_from_js():
    """Load track data from static/js/tracks.js file"""
    tracks_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'js', 'tracks.js')
    try:
        with open(tracks_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Extract the array from window.TRACKS = [...]
        match = re.search(r'window\.TRACKS\s*=\s*(\[.*?\]);', content, re.DOTALL)
        if match:
            tracks_json = match.group(1)
            return json.loads(tracks_json)
    except Exception as e:
        print(f"Error loading tracks: {e}")
    return []


# Load tracks from static/js/tracks.js
TRACKS = load_tracks_from_js()

# Data directory for storing user data
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def load_user_data(filename, default=None):
    """Load user data from JSON file"""
    if default is None:
        default = []
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return default
    return default


def save_user_data(filename, data):
    """Save user data to JSON file"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/tracks')
def get_tracks():
    """Get all tracks"""
    return jsonify(TRACKS)


@app.route('/api/tracks/<int:track_id>')
def get_track(track_id):
    """Get a specific track by ID"""
    for track in TRACKS:
        if track['id'] == track_id:
            return jsonify(track)
    return jsonify({'error': 'Track not found'}), 404


@app.route('/api/search')
def search_tracks():
    """Search tracks by query"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify(TRACKS)
    
    results = []
    for track in TRACKS:
        if query in track['title'].lower() or query in track['artist'].lower():
            results.append(track)
    return jsonify(results)


@app.route('/api/favorites', methods=['GET', 'POST'])
def favorites():
    """Get or update favorite tracks"""
    if request.method == 'GET':
        data = load_user_data('favorites.json', [])
        return jsonify(data)
    elif request.method == 'POST':
        data = request.json
        save_user_data('favorites.json', data)
        return jsonify({'success': True})


@app.route('/api/history', methods=['GET', 'POST'])
def history():
    """Get or update listening history"""
    if request.method == 'GET':
        data = load_user_data('history.json', [])
        return jsonify(data)
    elif request.method == 'POST':
        data = request.json
        save_user_data('history.json', data)
        return jsonify({'success': True})


@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    """Get or update user settings"""
    if request.method == 'GET':
        data = load_user_data('settings.json', {
            'theme': 'auto',
            'volume': 0.8,
            'shuffle': False,
            'repeatMode': 0
        })
        return jsonify(data)
    elif request.method == 'POST':
        data = request.json
        save_user_data('settings.json', data)
        return jsonify({'success': True})


@app.route('/api/playlist', methods=['GET', 'POST'])
def user_playlist():
    """Get or update user playlists"""
    if request.method == 'GET':
        data = load_user_data('playlists.json', [])
        return jsonify(data)
    elif request.method == 'POST':
        data = request.json
        save_user_data('playlists.json', data)
        return jsonify({'success': True})


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)


@app.route('/favicon/<path:filename>')
def serve_favicon(filename):
    """Serve favicon files"""
    return send_from_directory('static/favicon', filename)


if __name__ == '__main__':
    print("=" * 50)
    print("🎵 MusicPro.com Python Edition")
    print("=" * 50)
    print(f"Loaded {len(TRACKS)} tracks from static/js/tracks.js")
    print("Starting server...")
    print("Open http://localhost:5000 in your browser")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
