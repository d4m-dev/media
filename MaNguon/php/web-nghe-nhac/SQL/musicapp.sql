-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: sql309.byetcluster.com
-- Thời gian đã tạo: Th7 25, 2025 lúc 12:15 AM
-- Phiên bản máy phục vụ: 11.4.7-MariaDB
-- Phiên bản PHP: 7.2.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `if0_39253495_musicapp`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `comments`
--

CREATE TABLE `comments` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `song_id` int(11) DEFAULT NULL,
  `content` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `comments`
--

INSERT INTO `comments` (`id`, `user_id`, `song_id`, `content`, `created_at`) VALUES
(11, NULL, 1, 'Hi', '2025-07-06 10:44:56');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `favorites`
--

CREATE TABLE `favorites` (
  `user_id` int(11) NOT NULL,
  `song_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `favorites`
--

INSERT INTO `favorites` (`user_id`, `song_id`) VALUES
(4, 1),
(5, 1),
(1, 2),
(4, 3),
(5, 3),
(9, 4),
(10, 5),
(4, 8),
(4, 9),
(5, 9);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `genres`
--

CREATE TABLE `genres` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `genres`
--

INSERT INTO `genres` (`id`, `name`, `description`) VALUES
(1, 'OST', 'Nhạc phim, nhạc chủ đề từ điện ảnh hoặc truyền hình'),
(2, 'Remix', 'Các bản phối lại sôi động, thường có beat mạnh'),
(3, 'Lofi', 'Giai điệu nhẹ nhàng, thư giãn, thường dùng để học tập'),
(4, 'Official', 'Bản phát hành chính thức từ nghệ sĩ hoặc hãng đĩa'),
(5, 'Cover', 'Bài hát được hát lại bởi nghệ sĩ khác'),
(6, 'Nhạc Trung', 'Nhạc Hoa ngữ hoặc có nguồn gốc từ Trung Quốc'),
(7, 'Hát Live', 'Ghi âm từ sân khấu biểu diễn trực tiếp'),
(8, 'Mashup', 'Pha trộn nhiều bài hát lại thành một bản phối'),
(9, 'Ballad', 'Giai điệu chậm, cảm xúc, thường nói về tình yêu');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `likes_dislikes`
--

CREATE TABLE `likes_dislikes` (
  `user_id` int(11) NOT NULL,
  `song_id` int(11) NOT NULL,
  `action` enum('like','dislike') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `listening_history`
--

CREATE TABLE `listening_history` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `song_id` int(11) NOT NULL,
  `listened_at` datetime DEFAULT current_timestamp()
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `password_reset`
--

CREATE TABLE `password_reset` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `otp_code` varchar(6) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `expired_at` timestamp NOT NULL DEFAULT (current_timestamp() + interval 15 minute),
  `is_used` tinyint(1) DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `password_reset`
--

INSERT INTO `password_reset` (`id`, `user_id`, `otp_code`, `created_at`, `expired_at`, `is_used`) VALUES
(1, 5, '243793', '2025-06-24 12:21:47', '2025-06-24 12:36:47', 0),
(2, 6, '992394', '2025-06-29 22:58:20', '2025-06-29 23:13:20', 0);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `playlists`
--

CREATE TABLE `playlists` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `createdat` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `playlists`
--

INSERT INTO `playlists` (`id`, `user_id`, `name`, `createdat`) VALUES
(2, 4, 'Playlist Admin 1', '2025-06-24 14:21:33'),
(3, 1, 'Playlist vantoan123123', '2025-06-24 14:21:33'),
(4, 5, 'Playlist lyanan1609', '2025-06-24 14:21:33'),
(5, 9, 'Playlist ananly112', '2025-06-24 14:21:33'),
(6, 10, 'Playlist ananly122', '2025-06-24 14:21:33'),
(9, 5, 'Ngày mới', '2025-06-26 14:33:48');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `playlist_items`
--

CREATE TABLE `playlist_items` (
  `id` int(11) NOT NULL,
  `playlist_id` int(11) NOT NULL,
  `song_id` int(11) NOT NULL,
  `added_time` datetime DEFAULT current_timestamp()
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `playlist_items`
--

INSERT INTO `playlist_items` (`id`, `playlist_id`, `song_id`, `added_time`) VALUES
(16, 2, 1, '2025-07-08 06:43:30'),
(3, 2, 9, '2025-06-25 06:39:11'),
(5, 2, 11, '2025-06-25 07:10:20'),
(15, 2, 8, '2025-06-27 06:26:26'),
(14, 2, 3, '2025-06-27 06:26:13'),
(10, 9, 13, '2025-06-26 07:33:48');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `ratings`
--

CREATE TABLE `ratings` (
  `user_id` int(11) NOT NULL,
  `song_id` int(11) NOT NULL,
  `rating` int(11) DEFAULT NULL
) ;

--
-- Đang đổ dữ liệu cho bảng `ratings`
--

INSERT INTO `ratings` (`user_id`, `song_id`, `rating`) VALUES
(4, 1, 5),
(1, 2, 4),
(5, 3, 3),
(9, 4, 2),
(10, 5, 5);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `songs`
--

CREATE TABLE `songs` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `artist` varchar(255) NOT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `lyrics` text DEFAULT NULL,
  `file_path` varchar(255) NOT NULL,
  `cover_path` varchar(255) DEFAULT NULL,
  `views` int(11) DEFAULT 0,
  `uploaded_time` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `songs`
--

INSERT INTO `songs` (`id`, `title`, `artist`, `genre`, `lyrics`, `file_path`, `cover_path`, `views`, `uploaded_time`) VALUES
(1, 'Hay Là Chúng Ta Cứ Như Vậy Một Vạn Năm', 'Hoàng Tiêu Vân | Trường Nguyệt Tẫn Minh OST', 'OST', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/cunhuvaymotvannam/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/cunhuvaymotvannam/2.mp3', 'https://i.postimg.cc/sfB4vtbq/1.jpg', 110, '2025-06-20 09:30:50'),
(2, 'Em Đồng Ý | I Do', 'ĐỨC PHÚC x 911 x KHẮC HƯNG OFFICIAL', 'Official', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/weddingsongs/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/weddingsongs/ido.mp3', 'https://i.postimg.cc/TYDMgYZM/1.jpg', 55, '2025-06-20 09:30:50'),
(3, 'Vở Kịch Của Em x Vây Giữ REMIX', 'Hồ Phong An x HuyN FT', 'Remix', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/vokichcuaem/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/vokichcuaem/2.mp3', 'https://i.postimg.cc/SQCRjdNk/1.jpg', 50, '2025-06-20 09:30:50'),
(4, 'Yêu Em Nhưng Không Với Tới x Vây Giữ REMIX', 'DC Tâm x SS x AM Remix', 'Remix', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/yeuemnhungkhongvoitoi/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/yeuemnhungkhongvoitoi/2.mp3', 'https://i.postimg.cc/8PTpcV0m/1.jpg', 17, '2025-06-20 09:30:50'),
(5, 'Anh Đau Từ Lúc Em Đi REMIX', 'Trần Mạnh Cường', 'Remix', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/anhdautulucemdi/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/anhdautulucemdi/2.mp3', 'https://i.postimg.cc/5t3nSLmr/1.jpg', 17, '2025-06-20 09:30:50'),
(6, 'Mạnh Bà lofi', 'Linh Hương Luz', 'Lofi', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/manhba/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/manhba/2.mp3', 'https://i.postimg.cc/B62DC0sn/1.jpg', 10, '2025-06-20 09:30:50'),
(7, 'Địa Đàng REMIX', 'Hoàng Oanh x ACV', 'Remix', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/diadang/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/diadang/2.mp3', 'https://i.postimg.cc/GhwgrL9q/1.jpg', 20, '2025-06-20 09:30:50'),
(8, 'Tái Sinh REMIX', 'Tùng Dương x ACV', 'Remix', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/taisinh/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/taisinh/2.mp3', 'https://i.postimg.cc/mk0vWCJw/1.jpg', 28, '2025-06-20 09:30:50'),
(9, 'Ải Hồng Nhan REMIX', 'Cần Vinh x Lee Ken', 'Remix', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/aihongnhan/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/aihongnhan/2.mp3', 'https://i.postimg.cc/7hLc2m8X/1.jpg', 32, '2025-06-20 09:30:50'),
(10, 'Thương Thì Thôi REMIX', 'Jank', 'Remix', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/thuongthithoi/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/thuongthithoi/2.mp3', 'https://i.postimg.cc/v8Wk4gJp/1.jpg', 10, '2025-06-20 09:30:50'),
(11, 'Ba Kiếp Tình Một Kiếp Duyên lofi', 'Lâm Tuấn x MewMew lofi', 'Official', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/bakieptinhmotkiepduyen/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/bakieptinhmotkiepduyen/2.mp3', 'https://i.postimg.cc/K85HJ6GQ/1.jpg', 7, '2025-06-20 09:30:50'),
(12, 'Trả Lại Thanh Xuân Cho Em REMIX', 'Mochiii x Domino Remix', 'Remix', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/tralaithanhxuanchoem/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/tralaithanhxuanchoem/2.mp3', 'https://i.postimg.cc/4d3yYRd0/1.jpg', 8, '2025-06-20 09:30:50'),
(13, 'Đào Hoa Nặc', '旺仔小乔', 'Nhạc Trung', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/daohoanac/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/daohoanac/2.mp3', 'https://i.postimg.cc/htC0JcPF/1.jpg', 4, '2025-06-20 09:30:50'),
(14, 'Vây Giữ', 'Vương Tĩnh Văn', 'Nhạc Trung', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/vaygiu/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/vaygiu/2.mp3', 'https://i.postimg.cc/wx1byWs1/1.jpg', 2, '2025-06-20 09:30:50'),
(15, 'Khóa Ly Biệt Live', 'Anh Tú', 'Hát Live', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/khoalybiet/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/khoalybiet/2.mp3', 'https://i.postimg.cc/3NMRVV3b/1.jpg', 3, '2025-06-20 09:30:50'),
(16, 'Anh Thôi Nhân Nhượng Cover', 'Linh Hương Luz', 'Cover', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/anhthoinhanhuong/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/anhthoinhannhuong/2.mp3', 'https://i.postimg.cc/05cDXG3G/1.jpg', 11, '2025-06-20 09:30:50'),
(17, 'Nơi Đâu Tìm Thấy Em lofi', 'Chu Bin', 'Lofi', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/noidautimthayem/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/noidautimthayem/2.mp3', 'https://i.postimg.cc/tJzQQ37W/1.jpg', 6, '2025-06-20 09:30:50'),
(18, 'E Là Không Thể', 'Anh Quân x Đông Thiên Đức', 'Official', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/elakhongthe/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/elakhongthe/2.mp3', 'https://i.postimg.cc/tJ8PbxfR/1.jpg', 8, '2025-06-20 09:30:50'),
(19, 'Mashup 6 in 1', 'Mochiii Cover', 'Mashup', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/mashup6in1/1.lrc', 'https://upnhanh.us/files/f8c826d4d62d9e166e12ac4877bafc93/c9097511455de58ce9dba0203ac0f5f5/mashup6in1mochiii.mp3', 'https://i.postimg.cc/MZ7GFBLq/1.jpg', 8, '2025-06-20 09:30:50'),
(20, 'Cạn Tình Như Thế', 'Dickson x Thành Đạt', 'Official', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/cantinhnhuthe/1.lrc', 'https://github.com/d4m-dev/media/raw/refs/heads/main/cantinhnhuthe/2.mp3', 'https://i.postimg.cc/MHZ67gf9/1.jpg', 21, '2025-06-20 09:30:50');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `subscription_plans`
--

CREATE TABLE `subscription_plans` (
  `id` int(11) NOT NULL,
  `plan_name` varchar(100) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `duration` int(11) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `subscription_plans`
--

INSERT INTO `subscription_plans` (`id`, `plan_name`, `price`, `duration`, `description`, `created_at`, `updated_at`) VALUES
(1, 'free', '0.00', 30, 'Gói thuê bao miễn phí cho người dùng thường.', '2025-06-26 07:41:56', '2025-06-26 07:41:56'),
(2, 'premium', '0.99', 30, 'Gói thuê bao trả phí cho người quản trị với giá 0.99 USD.', '2025-06-26 07:41:56', '2025-06-26 07:41:56');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `role` enum('user','admin') DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `avatar` varchar(255) DEFAULT 'default-avatar.png'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `email`, `role`, `created_at`, `avatar`) VALUES
(1, 'vantoan123123', '$2y$10$I9KLfkslWDSxAJdOcMohOu2LdqtkEO4i90YPnf.4tDxiY/5myr3Pq', NULL, 'user', '2025-06-19 09:49:41', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/avatar/default-avatar.png'),
(4, 'admin', '$2y$10$c7QhxiSqxbDqwiC55PhpNOW6Xipjm7pJDNdfff5MtTKixNz8AqW5C', NULL, 'admin', '2025-06-20 09:26:26', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/avatar/default-avatar.png'),
(5, 'lyanan1609', '$2y$10$63gXtZFtK3c6OqZl/C0c0uPwCEDnvsqxvNdpuHj1saL6IOSoioirq', 'andurex5555@gmail.com', 'user', '2025-06-24 12:21:21', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/avatar/default-avatar.png'),
(6, 'mediaplayer123', '$2y$10$H9C7HLcn10LK1QUURQrMheiCMWUMVtZo75sAigtY/nJCqbIR0URha', 'admin@musicplatform.com', 'user', '2025-06-24 13:12:43', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/avatar/default-avatar.png'),
(7, 'admin1', '$2y$10$M.JHfkLHvYzaKYZgTQu2R.PPIcHHLezTXOAeV/3gZVXLCIPZFqcLW', 'abc@gmail.com', 'user', '2025-06-24 13:16:49', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/avatar/default-avatar.png'),
(8, 'thanhbuffgame', '$2y$10$MbyP42Rpr4KwDOgWddDIyuQN6vVoZX1NppPUdgrsJDRmoR0wwxGRO', 'thanh@gmail.com', 'user', '2025-06-24 13:18:45', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/avatar/default-avatar.png'),
(9, 'ananly112', '$2y$10$AYeunAxjcnxM.j9nCSLGN.Wi8ylen.JSOceI7HMjSc52yKwm8Bnou', 'anly@gmail.com', 'user', '2025-06-24 13:22:14', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/avatar/default-avatar.png'),
(10, 'ananly122', '$2y$10$FsZ5/lvuCJbIBX6YLOLiVOtVrG50S2LwD7dkdZ.0v7MUwrFC4fBTq', 'anly122@gmail.com', 'user', '2025-06-24 13:25:51', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/avatar/default-avatar.png'),
(11, 'hihiad', '$2y$10$Qfw.fhAinoqvZQGYECUnfOBT3JeT3Vm0uA/j2UcoMQ25mTzn.xP/6', 'hihi@gmail.com', 'user', '2025-06-24 13:30:41', 'https://raw.githubusercontent.com/d4m-dev/media/refs/heads/main/avatar/default-avatar.png');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `user_subscriptions`
--

CREATE TABLE `user_subscriptions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `plan_id` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `status` enum('active','expired','cancelled') DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `user_subscriptions`
--

INSERT INTO `user_subscriptions` (`id`, `user_id`, `plan_id`, `start_date`, `end_date`, `status`, `created_at`, `updated_at`) VALUES
(1, 4, 2, '2025-06-26', '2025-07-26', 'active', '2025-06-26 08:26:57', '2025-06-26 08:26:57'),
(3, 5, 2, '2025-06-26', '2025-07-26', 'active', '2025-06-26 14:27:54', '2025-06-26 14:27:54');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `song_id` (`song_id`);

--
-- Chỉ mục cho bảng `favorites`
--
ALTER TABLE `favorites`
  ADD PRIMARY KEY (`user_id`,`song_id`),
  ADD KEY `song_id` (`song_id`);

--
-- Chỉ mục cho bảng `genres`
--
ALTER TABLE `genres`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Chỉ mục cho bảng `likes_dislikes`
--
ALTER TABLE `likes_dislikes`
  ADD PRIMARY KEY (`user_id`,`song_id`),
  ADD KEY `fk_song` (`song_id`);

--
-- Chỉ mục cho bảng `listening_history`
--
ALTER TABLE `listening_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `song_id` (`song_id`);

--
-- Chỉ mục cho bảng `password_reset`
--
ALTER TABLE `password_reset`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Chỉ mục cho bảng `playlists`
--
ALTER TABLE `playlists`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Chỉ mục cho bảng `playlist_items`
--
ALTER TABLE `playlist_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `playlist_id` (`playlist_id`),
  ADD KEY `song_id` (`song_id`);

--
-- Chỉ mục cho bảng `songs`
--
ALTER TABLE `songs`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `subscription_plans`
--
ALTER TABLE `subscription_plans`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Chỉ mục cho bảng `user_subscriptions`
--
ALTER TABLE `user_subscriptions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `plan_id` (`plan_id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `comments`
--
ALTER TABLE `comments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT cho bảng `genres`
--
ALTER TABLE `genres`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT cho bảng `listening_history`
--
ALTER TABLE `listening_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `password_reset`
--
ALTER TABLE `password_reset`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT cho bảng `playlists`
--
ALTER TABLE `playlists`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT cho bảng `playlist_items`
--
ALTER TABLE `playlist_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT cho bảng `songs`
--
ALTER TABLE `songs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT cho bảng `subscription_plans`
--
ALTER TABLE `subscription_plans`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT cho bảng `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT cho bảng `user_subscriptions`
--
ALTER TABLE `user_subscriptions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `likes_dislikes`
--
ALTER TABLE `likes_dislikes`
  ADD CONSTRAINT `fk_song` FOREIGN KEY (`song_id`) REFERENCES `songs` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
