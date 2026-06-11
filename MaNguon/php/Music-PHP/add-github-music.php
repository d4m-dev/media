<?php
// Script để thêm nhạc từ GitHub vào database
include("includes/config.php");

// Xóa dữ liệu cũ
mysqli_query($con, "DELETE FROM Songs");
mysqli_query($con, "DELETE FROM albums");
mysqli_query($con, "DELETE FROM artists");

// Thêm artists
$artists = [
    "Hoàng Tiêu Vân",
    "ĐỨC PHÚC",
    "Hồ Phong An",
    "DC Tâm",
    "Trần Mạnh Cường",
    "Linh Hương Luz",
    "Hoàng Oanh",
    "Tùng Dương",
    "Cần Vinh",
    "Jank",
    "Lâm Tuấn",
    "旺仔小乔",
    "Vương Tĩnh Văn",
    "Anh Tú",
    "Chu Bin",
    "Anh Quân",
    "Mochiii",
    "Dickson",
    "Rumun Cover",
    "Pinky Vanh",
    "Thái Học",
    "Ca Sĩ Giấu Mặt",
    "HOAPROX",
    "Lê Gia Bảo",
    "Tú Na",
    "Út Nhị Mino",
    "DanhK",
    "Hanna Cẩm Tiên",
    "Hồ Phi Nal",
    "Nal",
    "Phạm Kỳ",
    "Dương Ái Vy",
    "Nana Liu",
    "Đạt Long Vinh",
    "Thành Đạt"
];

foreach ($artists as $index => $artistName) {
    $id = $index + 1;
    mysqli_query($con, "INSERT INTO artists (id, name) VALUES ('$id', '$artistName')");
}

// Thêm album mặc định
mysqli_query($con, "INSERT INTO albums (id, title, artist, genre, artworkPath) VALUES 
    (1, 'GitHub Music Collection', 1, 2, 'https://github.com/d4m-dev/media/raw/main/music/cunhuvaymotvannam/cover.jpg')");

// Thêm songs từ GitHub
$songs = [
    ["Hay Là Chúng Ta Cứ Như Vậy Một Vạn Năm", 1, "https://github.com/d4m-dev/media/raw/main/music/cunhuvaymotvannam/2.mp3", "2:37", 1],
    ["Em Đồng Ý | I Do", 2, "https://github.com/d4m-dev/media/raw/main/music/weddingsongs/2.mp3", "2:35", 2],
    ["Vở Kịch Của Em x Vây Giữ REMIX", 3, "https://github.com/d4m-dev/media/raw/main/music/vokichcuaem/2.mp3", "3:07", 3],
    ["Yêu Em Nhưng Không Với Tới x Vây Giữ REMIX", 4, "https://github.com/d4m-dev/media/raw/main/music/yeuemnhungkhongvoitoi/2.mp3", "3:08", 4],
    ["Anh Đau Từ Lúc Em Đi", 5, "https://github.com/d4m-dev/media/raw/main/music/anhdautulucemdi/2.mp3", "2:28", 5],
    ["Mạnh Bà Lofi", 6, "https://github.com/d4m-dev/media/raw/main/music/manhba/2.mp3", "4:21", 6],
    ["Địa Đàng REMIX", 7, "https://github.com/d4m-dev/media/raw/main/music/diadang/2.mp3", "2:58", 7],
    ["Tái Sinh REMIX", 8, "https://github.com/d4m-dev/media/raw/main/music/taisinh/2.mp3", "3:32", 8],
    ["Ải Hồng Nhan REMIX", 9, "https://github.com/d4m-dev/media/raw/main/music/aihongnhan/2.mp3", "2:43", 9],
    ["Thương Thì Thôi REMIX", 10, "https://github.com/d4m-dev/media/raw/main/music/thuongthithoi/2.mp3", "2:42", 10],
    ["Ba Kiếp Tình Một Kiếp Duyên Lofi", 11, "https://github.com/d4m-dev/media/raw/main/music/bakieptinhmotkiepduyen/2.mp3", "3:36", 11],
    ["Trả Lại Thanh Xuân Cho Em REMIX", 12, "https://github.com/d4m-dev/media/raw/main/music/tralaithanhxuanchoem/2.mp3", "2:20", 12],
    ["Đào Hoa Nặc", 13, "https://github.com/d4m-dev/media/raw/main/music/daohoanac/2.mp3", "5:07", 13],
    ["Vây Giữ", 14, "https://github.com/d4m-dev/media/raw/main/music/vaygiu/2.mp3", "2:03", 14],
    ["Khóa Ly Biệt Live", 15, "https://github.com/d4m-dev/media/raw/main/music/khoalybiet/2.mp3", "4:44", 15],
    ["Anh Thôi Nhân Nhượng Cover", 16, "https://github.com/d4m-dev/media/raw/main/music/anhthoinhannhuong/2.mp3", "3:26", 16],
    ["Nơi Đâu Tìm Thấy Em Lofi", 17, "https://github.com/d4m-dev/media/raw/main/music/noidautimthayem/2.mp3", "2:26", 17],
    ["E Là Không Thể", 18, "https://github.com/d4m-dev/media/raw/main/music/elakhongthe/2.mp3", "4:54", 18],
    ["Mashup 6 in 1", 19, "https://github.com/d4m-dev/media/raw/main/music/mashup6in1/2.mp3", "2:37", 19],
    ["Cạn Tình Như Thế", 20, "https://github.com/d4m-dev/media/raw/main/music/cantinhnhuthe/2.mp3", "2:35", 20],
    ["O Zon Dragostea Din Tei", 21, "https://github.com/d4m-dev/media/raw/main/music/o-zone-dragostea-din-tei-RumunCover/2.mp3", "3:07", 21],
    ["Người Lạ Từng Thương Remix", 22, "https://github.com/d4m-dev/media/raw/main/music/nguoilatungthuong/2.mp3", "3:08", 22],
    ["Nhạc Tết Miền Tây Remix", 23, "https://github.com/d4m-dev/media/raw/main/music/nhactetmientayremix/2.mp3", "2:28", 23],
    ["Họa Sĩ Tồi", 24, "https://github.com/d4m-dev/media/raw/main/music/hoasitoi/2.mp3", "4:21", 24],
    ["Thiệp Hồng Sai Tên", 25, "https://github.com/d4m-dev/media/raw/main/music/thiephongsaiten/2.mp3", "2:58", 25],
    ["Em Thua Cô Ta", 26, "https://github.com/d4m-dev/media/raw/main/music/emthuacota/2.mp3", "3:32", 26],
    ["WITH YOU (NGẪU HỨNG)", 27, "https://github.com/d4m-dev/media/raw/main/music/withyou-ngauhung/2.mp3", "2:43", 27],
    ["Tình Yêu Không Có Lỗi", 28, "https://github.com/d4m-dev/media/raw/main/music/tinhyeukhongcoloi/2.mp3", "2:42", 28],
    ["10 Mất 1 Còn Không", 29, "https://github.com/d4m-dev/media/raw/main/music/10mat1con0/2.mp3", "3:36", 29],
    ["Rời Remix", 30, "https://github.com/d4m-dev/media/raw/main/music/roi/2.mp3", "2:20", 30],
    ["Mãi Là Cô Dâu Của Anh", 31, "https://github.com/d4m-dev/media/raw/main/music/mailacodaucuaanh/2.mp3", "5:07", 31],
    ["Chẳng Thể Cảm Hóa", 32, "https://github.com/d4m-dev/media/raw/main/music/changthecamhoa/2.mp3", "2:03", 32],
    ["Hoa", 33, "https://github.com/d4m-dev/media/raw/main/music/hoa/2.mp3", "4:44", 33],
    ["Chờ Bao Lâu", 34, "https://github.com/d4m-dev/media/raw/main/music/chobaolau/2.mp3", "3:26", 34],
    ["Bắt Con Bướm Vàng", 35, "https://github.com/d4m-dev/media/raw/main/music/batconbuomvang/2.mp3", "2:26", 35],
    ["Đi Về Quê", 36, "https://github.com/d4m-dev/media/raw/main/music/diveque/2.mp3", "4:54", 36],
    ["Có Em Anh Thắng Đời", 37, "https://github.com/d4m-dev/media/raw/main/music/coemanhthangdoi/2.mp3", "2:37", 37],
    ["Sự Ưu Tiên Của Em", 38, "https://github.com/d4m-dev/media/raw/main/music/suuutiencuaem/2.mp3", "2:35", 38],
    ["Tết Này Kết Đôi", 39, "https://github.com/d4m-dev/media/raw/main/music/tenayketdoi/2.mp3", "3:07", 39],
    ["Tết Này Có Nhau", 40, "https://github.com/d4m-dev/media/raw/main/music/tetnayconhau/2.mp3", "3:08", 40],
    ["Cưới Tết", 41, "https://github.com/d4m-dev/media/raw/main/music/cuoitet/2.mp3", "2:28", 41],
    ["Sợi Chỉ Hồng", 42, "https://github.com/d4m-dev/media/raw/main/music/soichihong/2.mp3", "4:21", 42],
    ["Mãnh Tình Sai Đôi", 43, "https://github.com/d4m-dev/media/raw/main/music/manhtinhsaidoi/2.mp3", "2:58", 43],
    ["Lệ Ngang Trời", 44, "https://github.com/d4m-dev/media/raw/main/music/lengangtroi/2.mp3", "3:32", 44],
    ["Phong Sương Tửu", 45, "https://github.com/d4m-dev/media/raw/main/music/phongsuongtuu/2.mp3", "2:43", 45],
    ["Rồi Nâng Cái Ly Lên", 46, "https://github.com/d4m-dev/media/raw/main/music/roinangcailylen/2.mp3", "2:42", 46],
    ["Xuân Vu Quy", 47, "https://github.com/d4m-dev/media/raw/main/music/xuanvuquy/2.mp3", "3:36", 47],
    ["Tự Em Sai", 48, "https://github.com/d4m-dev/media/raw/main/music/tuemsai/2.mp3", "2:20", 48],
    ["Anh Vui", 49, "https://github.com/d4m-dev/media/raw/main/music/anhvui/2.mp3", "2:37", 49],
    ["Bà Xã Của Anh", 50, "https://github.com/d4m-dev/media/raw/main/music/baxacuaanh/2.mp3", "2:35", 50],
    ["Cưới Chính", 51, "https://github.com/d4m-dev/media/raw/main/music/cuoichinh/2.mp3", "3:07", 51],
    ["Em Nhắc Anh", 52, "https://github.com/d4m-dev/media/raw/main/music/emnhacanh/2.mp3", "3:08", 52],
    ["Xuân Huy Hoàng", 53, "https://github.com/d4m-dev/media/raw/main/music/xuanhuyhoang/2.mp3", "2:28", 53],
    ["Hỏi Vợ Ngoại Thành Lofi", 54, "https://github.com/d4m-dev/media/raw/main/music/hoivongoaithanh/2.mp3", "4:21", 54]
];

foreach ($songs as $index => $song) {
    $id = $index + 1;
    $title = $song[0];
    $artistId = $song[1];
    $path = $song[2];
    $duration = $song[3];
    $albumOrder = $song[4];
    
    mysqli_query($con, "INSERT INTO Songs (id, title, artist, album, genre, duration, path, albumOrder, plays) 
        VALUES ('$id', '$title', '$artistId', 1, 2, '$duration', '$path', '$albumOrder', 0)");
}

echo "Đã thêm " . count($songs) . " bài hát từ GitHub vào database!";
?>
