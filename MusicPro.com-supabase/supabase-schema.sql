-- Supabase Database Schema for Music Pro Application

-- Table for music tracks
CREATE TABLE IF NOT EXISTS tracks (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    cover TEXT,
    audio_src TEXT,
    instrumental_src TEXT,
    video_src TEXT,
    lyric_src TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Enable Row Level Security (RLS) on tracks
ALTER TABLE tracks ENABLE ROW LEVEL SECURITY;

-- Policy to allow anyone to view tracks (public read)
CREATE POLICY "Anyone can view tracks" ON tracks
    FOR SELECT TO authenticated, anon USING (true);

-- Policy to allow service role to manage tracks (for admin operations)
CREATE POLICY "Service role can manage tracks" ON tracks
    FOR ALL TO service_role USING (true);

-- Table for user profiles
CREATE TABLE IF NOT EXISTS user_profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    custom_primary_color TEXT,
    font_family TEXT,
    font_weight TEXT DEFAULT '400',
    layout_mode TEXT DEFAULT 'standard',
    user_name TEXT,
    user_email TEXT,
    user_avatar TEXT
);

-- Enable Row Level Security (RLS) on user_profiles
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Policy to allow users to only access their own profile
CREATE POLICY "Users can view own profile" ON user_profiles
    FOR SELECT USING (auth.uid()::text = user_id OR auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can insert own profile" ON user_profiles
    FOR INSERT WITH CHECK (auth.uid()::text = user_id OR auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can update own profile" ON user_profiles
    FOR UPDATE USING (auth.uid()::text = user_id OR auth.jwt() ->> 'email' = user_email);

-- Table for user playlists
CREATE TABLE IF NOT EXISTS user_playlists (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    playlist_name TEXT NOT NULL,
    playlist_description TEXT,
    playlist_tracks TEXT[] DEFAULT '{}'
);

-- Enable Row Level Security (RLS) on user_playlists
ALTER TABLE user_playlists ENABLE ROW LEVEL SECURITY;

-- Policy to allow users to only access their own playlists
CREATE POLICY "Users can view own playlists" ON user_playlists
    FOR SELECT USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert own playlists" ON user_playlists
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can update own playlists" ON user_playlists
    FOR UPDATE USING (auth.uid()::text = user_id);

CREATE POLICY "Users can delete own playlists" ON user_playlists
    FOR DELETE USING (auth.uid()::text = user_id);

-- Table for user favorites
CREATE TABLE IF NOT EXISTS user_favorites (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    favorite_tracks TEXT[] DEFAULT '{}'
);

-- Enable Row Level Security (RLS) on user_favorites
ALTER TABLE user_favorites ENABLE ROW LEVEL SECURITY;

-- Policy to allow users to only access their own favorites
CREATE POLICY "Users can view own favorites" ON user_favorites
    FOR SELECT USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert own favorites" ON user_favorites
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can update own favorites" ON user_favorites
    FOR UPDATE USING (auth.uid()::text = user_id);

-- Function to update the 'updated_at' timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers to automatically update the 'updated_at' timestamp
CREATE TRIGGER update_tracks_updated_at 
    BEFORE UPDATE ON tracks 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at 
    BEFORE UPDATE ON user_profiles 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_playlists_updated_at 
    BEFORE UPDATE ON user_playlists 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_favorites_updated_at 
    BEFORE UPDATE ON user_favorites 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Sample INSERT statements for tracks
-- These should be run in your Supabase SQL editor to populate the tracks table
-- Replace the sample data with your actual track data

INSERT INTO tracks (title, artist, cover, audio_src, instrumental_src, video_src, lyric_src) VALUES
('Hay Là Chúng Ta Cứ Như Vậy Một Vạn Năm', 'Hoàng Tiêu Vân | Trường Nguyệt Tẫn Minh OST', 'https://github.com/d4m-dev/media/raw/main/music/cunhuvaymotvannam/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/cunhuvaymotvannam/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/cunhuvaymotvannam/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/cunhuvaymotvannam/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/cunhuvaymotvannam/1.lrc'),
('Em Đồng Ý | I Do', 'ĐỨC PHÚC x 911 x KHẮC HƯNG OFFICIAL', 'https://github.com/d4m-dev/media/raw/main/music/weddingsongs/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/weddingsongs/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/weddingsongs/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/weddingsongs/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/weddingsongs/1.lrc'),
('Vở Kịch Của Em x Vây Giữ REMIX', 'Hồ Phong An x HuyN FT', 'https://github.com/d4m-dev/media/raw/main/music/vokichcuaem/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/vokichcuaem/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/vokichcuaem/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/vokichcuaem/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/vokichcuaem/1.lrc'),
('Yêu Em Nhưng Không Với Tới x Vây Giữ REMIX', 'DC Tâm x SS x AM Remix', 'https://github.com/d4m-dev/media/raw/main/music/yeuemnhungkhongvoitoi/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/yeuemnhungkhongvoitoi/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/yeuemnhungkhongvoitoi/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/yeuemnhungkhongvoitoi/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/yeuemnhungkhongvoitoi/1.lrc'),
('Anh Đau Từ Lúc Em Đi', 'Trần Mạnh Cường', 'https://github.com/d4m-dev/media/raw/main/music/anhdautulucemdi/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/anhdautulucemdi/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/anhdautulucemdi/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/anhdautulucemdi/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/anhdautulucemdi/1.lrc'),
('Mạnh Bà Lofi', 'Linh Hương Luz', 'https://github.com/d4m-dev/media/raw/main/music/manhba/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/manhba/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/manhba/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/manhba/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/manhba/1.lrc'),
('Địa Đàng REMIX', 'Hoàng Oanh x ACV', 'https://github.com/d4m-dev/media/raw/main/music/diadang/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/diadang/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/diadang/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/diadang/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/diadang/1.lrc'),
('Tái Sinh REMIX', 'Tùng Dương x ACV', 'https://github.com/d4m-dev/media/raw/main/music/taisinh/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/taisinh/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/taisinh/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/taisinh/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/taisinh/1.lrc'),
('Ải Hồng Nhan REMIX', 'Cần Vinh x Lee Ken', 'https://github.com/d4m-dev/media/raw/main/music/aihongnhan/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/aihongnhan/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/aihongnhan/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/aihongnhan/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/aihongnhan/1.lrc'),
('Thương Thì Thôi REMIX', 'Jank', 'https://github.com/d4m-dev/media/raw/main/music/thuongthithoi/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/thuongthithoi/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/thuongthithoi/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/thuongthithoi/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/thuongthithoi/1.lrc'),
('Ba Kiếp Tình Một Kiếp Duyên Lofi', 'Lâm Tuấn x MewMew Lofi', 'https://github.com/d4m-dev/media/raw/main/music/bakieptinhmotkiepduyen/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/bakieptinhmotkiepduyen/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/bakieptinhmotkiepduyen/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/bakieptinhmotkiepduyen/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/bakieptinhmotkiepduyen/1.lrc'),
('Trả Lại Thanh Xuân Cho Em REMIX', 'Mochiii x Domino Remix', 'https://github.com/d4m-dev/media/raw/main/music/tralaithanhxuanchoem/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/tralaithanhxuanchoem/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/tralaithanhxuanchoem/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/tralaithanhxuanchoem/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/tralaithanhxuanchoem/1.lrc'),
('Đào Hoa Nặc', '旺仔小乔', 'https://github.com/d4m-dev/media/raw/main/music/daohoanac/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/daohoanac/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/daohoanac/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/daohoanac/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/daohoanac/1.lrc'),
('Vây Giữ', 'Vương Tĩnh Văn', 'https://github.com/d4m-dev/media/raw/main/music/vaygiu/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/vaygiu/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/vaygiu/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/vaygiu/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/vaygiu/1.lrc'),
('Khóa Ly Biệt Live', 'Anh Tú', 'https://github.com/d4m-dev/media/raw/main/music/khoalybiet/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/khoalybiet/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/khoalybiet/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/khoalybiet/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/khoalybiet/1.lrc'),
('Anh Thôi Nhân Nhượng Cover', 'Linh Hương Luz', 'https://github.com/d4m-dev/media/raw/main/music/anhthoinhannhuong/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/anhthoinhannhuong/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/anhthoinhannhuong/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/anhthoinhannhuong/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/anhthoinhannhuong/1.lrc'),
('Nơi Đâu Tìm Thấy Em Lofi', 'Chu Bin', 'https://github.com/d4m-dev/media/raw/main/music/noidautimthayem/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/noidautimthayem/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/noidautimthayem/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/noidautimthayem/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/noidautimthayem/1.lrc'),
('E Là Không Thể', 'Anh Quân x Đông Thiên Đức', 'https://github.com/d4m-dev/media/raw/main/music/elakhongthe/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/elakhongthe/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/elakhongthe/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/elakhongthe/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/elakhongthe/1.lrc'),
('Mashup 6 in 1', 'Mochiii Cover', 'https://github.com/d4m-dev/media/raw/main/music/mashup6in1/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/mashup6in1/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/mashup6in1/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/mashup6in1/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/mashup6in1/1.lrc'),
('Cạn Tình Như Thế', 'Dickson x Thành Đạt', 'https://github.com/d4m-dev/media/raw/main/music/cantinhnhuthe/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/cantinhnhuthe/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/cantinhnhuthe/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/cantinhnhuthe/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/cantinhnhuthe/1.lrc'),
('O Zon Dragostea Din Tei', 'Rumun Cover', 'https://github.com/d4m-dev/media/raw/main/music/o-zone-dragostea-din-tei-RumunCover/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/o-zone-dragostea-din-tei-RumunCover/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/o-zone-dragostea-din-tei-RumunCover/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/o-zone-dragostea-din-tei-RumunCover/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/o-zone-dragostea-din-tei-RumunCover/1.lrc'),
('Người Lạ Từng Thương Remix', 'Mochii Cover', 'https://github.com/d4m-dev/media/raw/main/music/nguoilatungthuong/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/nguoilatungthuong/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/nguoilatungthuong/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/nguoilatungthuong/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/nguoilatungthuong/1.lrc'),
('Nhạc Tết Miền Tây Remix', 'Pinky Vanh x Hoa Vũ, H2K,...', 'https://github.com/d4m-dev/media/raw/main/music/nhactetmientayremix/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/nhactetmientayremix/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/nhactetmientayremix/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/nhactetmientayremix/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/nhactetmientayremix/1.lrc'),
('Họa Sĩ Tồi', 'Thái Học x Đạt Max', 'https://github.com/d4m-dev/media/raw/main/music/hoasitoi/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/hoasitoi/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/hoasitoi/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/hoasitoi/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/hoasitoi/1.lrc'),
('Thiệp Hồng Sai Tên', 'Mochii Cover', 'https://github.com/d4m-dev/media/raw/main/music/thiephongsaiten/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/thiephongsaiten/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/thiephongsaiten/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/thiephongsaiten/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/thiephongsaiten/1.lrc'),
('Em Thua Cô Ta', 'Ca Sĩ Giấu Mặt Cover', 'https://github.com/d4m-dev/media/raw/main/music/emthuacota/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/emthuacota/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/emthuacota/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/emthuacota/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/emthuacota/1.lrc'),
('WITH YOU (NGẪU HỨNG)', 'HOAPROX, NICK STRAND & MIO', 'https://github.com/d4m-dev/media/raw/main/music/withyou-ngauhung/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/withyou-ngauhung/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/withyou-ngauhung/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/withyou-ngauhung/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/withyou-ngauhung/1.lrc'),
('Tình Yêu Không Có Lỗi', 'Mochii', 'https://github.com/d4m-dev/media/raw/main/music/tinhyeukhongcoloi/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/tinhyeukhongcoloi/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/tinhyeukhongcoloi/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/tinhyeukhongcoloi/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/tinhyeukhongcoloi/1.lrc'),
('10 Mất 1 Còn Không', 'Lê Gia Bảo, BMZ', 'https://github.com/d4m-dev/media/raw/main/music/10mat1con0/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/10mat1con0/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/10mat1con0/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/10mat1con0/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/10mat1con0/1.lrc'),
('Rời Remix', 'Linh Hương Luz', 'https://github.com/d4m-dev/media/raw/main/music/roi/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/roi/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/roi/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/roi/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/roi/1.lrc'),
('Mãi Là Cô Dâu Của Anh', 'Mochii Cover', 'https://github.com/d4m-dev/media/raw/main/music/mailacodaucuaanh/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/mailacodaucuaanh/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/mailacodaucuaanh/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/mailacodaucuaanh/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/mailacodaucuaanh/1.lrc'),
('Chẳng Thể Cảm Hóa', 'Thái Học Cover', 'https://github.com/d4m-dev/media/raw/main/music/changthecamhoa/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/changthecamhoa/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/changthecamhoa/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/changthecamhoa/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/changthecamhoa/1.lrc'),
('Hoa', 'Tú Na Cover', 'https://github.com/d4m-dev/media/raw/main/music/hoa/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/hoa/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/hoa/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/hoa/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/hoa/1.lrc'),
('Chờ Bao Lâu', 'Út Nhị Mino, Hào JK', 'https://github.com/d4m-dev/media/raw/main/music/chobaolau/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/chobaolau/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/chobaolau/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/chobaolau/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/chobaolau/1.lrc'),
('Bắt Con Bướm Vàng', 'DanhK', 'https://github.com/d4m-dev/media/raw/main/music/batconbuomvang/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/batconbuomvang/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/batconbuomvang/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/batconbuomvang/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/batconbuomvang/1.lrc'),
('Đi Về Quê', 'Út Nhị Mino', 'https://github.com/d4m-dev/media/raw/main/music/diveque/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/diveque/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/diveque/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/diveque/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/diveque/1.lrc'),
('Có Em Anh Thắng Đời', 'Hanna Cẩm Tiên', 'https://github.com/d4m-dev/media/raw/main/music/coemanhthangdoi/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/coemanhthangdoi/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/coemanhthangdoi/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/coemanhthangdoi/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/coemanhthangdoi/1.lrc'),
('Sự Ưu Tiên Của Em', 'Lê Gia Bảo x Thái Học', 'https://github.com/d4m-dev/media/raw/main/music/suuutiencuaem/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/suuutiencuaem/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/suuutiencuaem/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/suuutiencuaem/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/suuutiencuaem/1.lrc'),
('Tết Này Kết Đôi', 'Pinky Vanh x Hoa Vũ', 'https://github.com/d4m-dev/media/raw/main/music/tenayketdoi/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/tenayketdoi/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/tenayketdoi/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/tenayketdoi/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/tenayketdoi/1.lrc'),
('Tết Này Có Nhau', 'Pinky Vanh x Hoa Vũ', 'https://github.com/d4m-dev/media/raw/main/music/tetnayconhau/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/tetnayconhau/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/tetnayconhau/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/tetnayconhau/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/tetnayconhau/1.lrc'),
('Cưới Tết', 'Hồ Phi Nal', 'https://github.com/d4m-dev/media/raw/main/music/cuoitet/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/cuoitet/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/cuoitet/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/cuoitet/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/cuoitet/1.lrc'),
('Sợi Chỉ Hồng | Cưới Vợ Cho Cha OST', 'Hanna Cẩm Tiên x Danhka', 'https://github.com/d4m-dev/media/raw/main/music/soichihong/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/soichihong/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/soichihong/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/soichihong/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/soichihong/1.lrc'),
('Mãnh Tình Sai Đôi', 'Mochii Cover', 'https://github.com/d4m-dev/media/raw/main/music/manhtinhsaidoi/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/manhtinhsaidoi/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/manhtinhsaidoi/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/manhtinhsaidoi/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/manhtinhsaidoi/1.lrc'),
('Lệ Ngang Trời', 'Ca Sĩ Giấu Mặt', 'https://github.com/d4m-dev/media/raw/main/music/lengangtroi/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/lengangtroi/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/lengangtroi/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/lengangtroi/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/lengangtroi/1.lrc'),
('Phong Sương Tửu', 'Ca Sĩ Giấu Mặt', 'https://github.com/d4m-dev/media/raw/main/music/phongsuongtuu/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/phongsuongtuu/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/phongsuongtuu/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/phongsuongtuu/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/phongsuongtuu/1.lrc'),
('Rồi Nâng Cái Ly Lên', 'Nal', 'https://github.com/d4m-dev/media/raw/main/music/roinangcailylen/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/roinangcailylen/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/roinangcailylen/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/roinangcailylen/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/roinangcailylen/1.lrc'),
('Xuân Vu Quy', 'DanhKa', 'https://github.com/d4m-dev/media/raw/main/music/xuanvuquy/cover.jpg', 'https://github.com/d4m-dev/media/raw/main/music/xuanvuquy/2.mp3', 'https://github.com/d4m-dev/media/raw/main/music/xuanvuquy/3.mp3', 'https://github.com/d4m-dev/media/raw/main/music/xuanvuquy/4.mp4', 'https://raw.githubusercontent.com/d4m-dev/media/main/music/xuanvuquy/1.lrc');