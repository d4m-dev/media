#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MusicPro.com Python Edition - Public Entry Point
Giao diện web chính cho ứng dụng MusicPro
"""

import sys
import os

# Lấy thư mục chứa file này (public/)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Thư mục gốc của project (MusicPro.com-python/)
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

# Thêm project dir vào path
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import re

# Khởi tạo Flask app với đường dẫn tuyệt đối
app = Flask(__name__,
            template_folder=os.path.join(PROJECT_DIR, 'templates'),
            static_folder=os.path.join(PROJECT_DIR, 'static'))

# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================

def load_tracks_from_js():
    """Load danh sách bài hát từ file static/js/tracks.js"""
    tracks_path = os.path.join(PROJECT_DIR, 'static', 'js', 'tracks.js')
    try:
        with open(tracks_path, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'window\.TRACKS\s*=\s*(\[.*?\]);', content, re.DOTALL)
        if match:
            tracks_json = match.group(1)
            return json.loads(tracks_json)
    except Exception as e:
        print(f"Lỗi khi load tracks: {e}")
    return []


# =============================================================================
# DATA DIRECTORY SETUP
# =============================================================================

DATA_DIR = os.path.join(PROJECT_DIR, 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def load_user_data(filename, default=None):
    """Load dữ liệu người dùng từ file JSON"""
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
    """Lưu dữ liệu người dùng vào file JSON"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Load tracks khi khởi động
TRACKS = load_tracks_from_js()


# =============================================================================
# ROUTES - TRANG WEB
# =============================================================================

@app.route('/')
def index():
    """Trang chủ - Giao diện chính của MusicPro"""
    return render_template('index.html')


# =============================================================================
# API ROUTES
# =============================================================================

@app.route('/api/tracks')
def get_tracks():
    """API: Lấy tất cả bài hát"""
    return jsonify(TRACKS)


@app.route('/api/tracks/<int:track_id>')
def get_track(track_id):
    """API: Lấy thông tin 1 bài hát theo ID"""
    for track in TRACKS:
        if track['id'] == track_id:
            return jsonify(track)
    return jsonify({'error': 'Không tìm thấy bài hát'}), 404


@app.route('/api/search')
def search_tracks():
    """API: Tìm kiếm bài hát theo tên/ca sĩ"""
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
    """API: Quản lý danh sách yêu thích"""
    if request.method == 'GET':
        data = load_user_data('favorites.json', [])
        return jsonify(data)
    elif request.method == 'POST':
        data = request.json
        save_user_data('favorites.json', data)
        return jsonify({'success': True})


@app.route('/api/history', methods=['GET', 'POST'])
def history():
    """API: Quản lý lịch sử nghe nhạc"""
    if request.method == 'GET':
        data = load_user_data('history.json', [])
        return jsonify(data)
    elif request.method == 'POST':
        data = request.json
        save_user_data('history.json', data)
        return jsonify({'success': True})


@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    """API: Quản lý cài đặt ứng dụng"""
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
    """API: Quản lý playlist người dùng"""
    if request.method == 'GET':
        data = load_user_data('playlists.json', [])
        return jsonify(data)
    elif request.method == 'POST':
        data = request.json
        save_user_data('playlists.json', data)
        return jsonify({'success': True})


# =============================================================================
# STATIC FILES - Custom handler để phục vụ static đúng cách
# =============================================================================

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Phục vụ file tĩnh từ project's static folder"""
    return send_from_directory(os.path.join(PROJECT_DIR, 'static'), filename)


@app.route('/favicon/<path:filename>')
def serve_favicon(filename):
    """Phục vụ favicon"""
    return send_from_directory(os.path.join(PROJECT_DIR, 'static', 'favicon'), filename)


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("🎵 MusicPro.com Python Edition")
    print("=" * 60)
    print(f"✅ Đã load {len(TRACKS)} bài hát từ static/js/tracks.js")
    print(f"📁 Thư mục dữ liệu: {DATA_DIR}")
    print("=" * 60)
    print("🚀 Đang khởi động server...")
    print("🌐 Mở trình duyệt tại: http://localhost:5000")
    print("=" * 60)
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )
