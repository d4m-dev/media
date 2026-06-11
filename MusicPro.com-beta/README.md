# Music Pro Ultimate

Dự án Music Pro Ultimate đã được cấu trúc và module hóa lại nhằm tăng tính bảo trì và khả năng mở rộng. File `app.js` nguyên khối lớn đã được tách thành các module nhỏ xử lý từng phần chuyên biệt.

## Cấu trúc thư mục mới

```text
/MusicPro.com-beta
├── index.html            # File giao diện chính, đã cập nhật để tải app.js như một ES Module (type="module")
├── README.md             # Tài liệu dự án (bạn đang đọc)
└── src/
    ├── app.js            # File khởi tạo chính, import các module và gắn vào class MusicPro
    ├── playlists.js      # Dữ liệu danh sách phát tĩnh
    ├── tracks.js         # Dữ liệu các bài hát tĩnh
    ├── styles.css        # File CSS giao diện chính
    ├── favicon/          # Chứa các icon, logo và webmanifest
    ├── font-style/       # Chứa các font chữ cục bộ dùng trong dự án
    └── modules/          # Chứa các tính năng đã được tách nhỏ từ app.js
        ├── audio.js      # Quản lý phát nhạc, hiệu ứng âm thanh, EQ và Audio Context
        ├── events.js     # Chứa các event handler cho UI và phím tắt
        ├── helpers.js    # Các hàm tiện ích hỗ trợ fetch data từ xa và chuẩn hóa (normalize)
        ├── lyrics.js     # Module xử lý lời bài hát, đồng bộ và hiển thị PiP (Picture-in-Picture)
        ├── other.js      # Logic của các tính năng phụ trợ (ví dụ: chia sẻ, download, hẹn giờ)
        ├── ui.js         # Quản lý hiển thị UI chính, render list, virtual scrolling, xử lý custom theme
        └── utils.js      # Các hàm tiện ích chung (ví dụ: formatTime, darkenColor)
```

## Luồng hoạt động

1. **`index.html`** gọi script `app.js` với thuộc tính `type="module"`.
2. **`src/app.js`** sẽ tự động import các đối tượng method từ thư mục `src/modules/`.
3. Trong **`app.js`**, class `MusicPro` được định nghĩa kèm constructor khởi tạo state.
4. Các phương thức từ các module (UI, Audio, Lyrics,...) được thêm vào prototype của `MusicPro` bằng `Object.assign`.
5. Cuối cùng, `window.app = new MusicPro();` được chạy để khởi động toàn bộ ứng dụng và gắn instance này vào `window` nhằm xử lý các event DOM inline (như `onclick="app.playIndex(...)"`).

Việc tái cấu trúc này giúp codebase dễ đọc hơn, dễ quản lý các tính năng hơn và dễ dàng sửa lỗi mà không làm ảnh hưởng đến các file khác trong hệ thống.
