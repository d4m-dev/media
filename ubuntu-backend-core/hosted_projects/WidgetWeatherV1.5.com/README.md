# WidgetWeather.com — Weather Widget (Embed Guide)

> Tài liệu này hướng dẫn cách **nhúng (embed) widget thời tiết** từ repo `d4m-dev/WidgetWeather.com` vào website của bạn, kèm mô tả chức năng và các lưu ý triển khai.

- **Repository:** https://github.com/d4m-dev/WidgetWeather.com citeturn1view0  
- **Demo (GitHub Pages):** https://d4m-dev.github.io/WidgetWeather.com/ citeturn10view1  

---

## Mục lục

- [Tổng quan](#tổng-quan)
- [Nhúng nhanh (khuyến nghị)](#nhúng-nhanh-khuyến-nghị)
- [Nhúng bằng placeholder (để chủ động vị trí)](#nhúng-bằng-placeholder-để-chủ-động-vị-trí)
- [Chức năng của widget](#chức-năng-của-widget)
- [Tối ưu giao diện & tránh vỡ layout](#tối-ưu-giao-diện--tránh-vỡ-layout)
- [Tự host (self-host) để tùy biến sâu](#tự-host-self-host-để-tùy-biến-sâu)
- [Khắc phục sự cố](#khắc-phục-sự-cố)
- [Bảo mật & lưu ý sản xuất](#bảo-mật--lưu-ý-sản-xuất)
- [License](#license)

---

## Tổng quan

WidgetWeather.com cung cấp một widget hiển thị thời tiết theo dạng “card” (thẻ thông tin) — phù hợp nhúng vào landing page, blog, portfolio, hoặc các trang nội dung.

Trong demo hiện tại, widget hiển thị các khối thông tin như:

- Nhiệt độ hiện tại
- “Cảm giác như” (feels like)
- Độ ẩm
- Gió
- Áp suất
- Dự báo nhiều ngày (trong demo có tiêu đề “Dự báo 5 ngày”) citeturn10view1

> Ghi chú: Demo có thông báo “Đang hiển thị dữ liệu mẫu (API Key hết hạn hoặc lỗi kết nối)” — nghĩa là widget có cơ chế **fallback dữ liệu mẫu** khi không lấy được dữ liệu thời tiết thật. citeturn10view1

---

## Nhúng nhanh (khuyến nghị)

Cách nhúng nhanh nhất là chèn **1 dòng script loader** (bạn đã đưa):

```html
<script src="https://d4m-dev.github.io/WidgetWeather.com/widget-loader.js"></script>
```

### Vị trí đặt script

Khuyến nghị đặt **cuối `<body>`** để tránh ảnh hưởng tốc độ tải trang:

```html
<!doctype html>
<html lang="vi">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Demo Weather Widget</title>
  </head>
  <body>
    <!-- Nội dung trang của bạn -->

    <!-- Weather Widget Loader -->
    <script src="https://d4m-dev.github.io/WidgetWeather.com/widget-loader.js"></script>
  </body>
</html>
```

### Khi nào nên đặt trong `<head>`?

Chỉ nên đặt trong `<head>` nếu bạn cần widget load sớm; khi đó nên dùng `defer` để không chặn render:

```html
<script defer src="https://d4m-dev.github.io/WidgetWeather.com/widget-loader.js"></script>
```

---

## Nhúng bằng placeholder (để chủ động vị trí)

Nếu bạn muốn chủ động **vị trí hiển thị widget** (khuyến nghị cho layout phức tạp), hãy tạo một “placeholder” trước, rồi load script.

Ví dụ:

```html
<div id="weather-widget"></div>

<script src="https://d4m-dev.github.io/WidgetWeather.com/widget-loader.js"></script>
```

> Nếu dự án loader của bạn dùng selector khác (ví dụ class thay vì id), bạn chỉ cần đổi tương ứng trong HTML.  
> (Trong repo, bạn có thể kiểm tra chính xác selector/target trong file loader.)

---

## Chức năng của widget

Dựa trên demo GitHub Pages, widget đang có các nhóm chức năng/hiển thị chính sau: citeturn10view1

### 1) Hiển thị thời tiết hiện tại

- Nhiệt độ (°C)
- Trạng thái thời tiết / mô tả ngắn (tuỳ cấu hình/nguồn dữ liệu)
- Các chỉ số phụ:
  - Cảm giác như (feels like)
  - Độ ẩm (%)
  - Tốc độ gió (km/h)
  - Áp suất (hPa)

### 2) Dự báo nhiều ngày

- Phần “Dự báo 5 ngày” cho phép hiển thị dự báo theo ngày (hoặc theo danh sách ngày). citeturn10view1

### 3) Trạng thái tải dữ liệu & fallback

- Có trạng thái “Đang tải dữ liệu...”
- Có trạng thái lỗi “Không thể tải dữ liệu”
- Có cơ chế hiển thị **dữ liệu mẫu** khi không lấy được dữ liệu thật (ví dụ API key hết hạn). citeturn10view1

---

## Tối ưu giao diện & tránh vỡ layout

### 1) Bọc widget trong một container có giới hạn

Khuyến nghị:

```html
<div class="weather-wrap">
  <div id="weather-widget"></div>
</div>
```

Và CSS:

```css
.weather-wrap {
  max-width: 520px;     /* bạn có thể tăng/giảm */
  margin: 0 auto;       /* căn giữa */
  padding: 8px;         /* tránh sát mép */
}
```

### 2) Tránh “layout shift” khi widget load

Bạn có thể đặt min-height tạm để tránh nhảy layout:

```css
#weather-widget {
  min-height: 280px; /* ước lượng theo UI của bạn */
}
```

### 3) Responsive trên mobile

- Ưu tiên container `width: 100%`
- Chừa padding hai bên (8–12px) để widget không chạm mép màn hình.

---

## Tự host (self-host) để tùy biến sâu

Nếu bạn muốn:
- đổi UI/CSS,
- chỉnh logic fetch,
- thay API provider,
- hoặc đóng gói theo dự án của bạn,

thì nên tự host:

1. Fork hoặc clone repo: `d4m-dev/WidgetWeather.com` citeturn1view0  
2. Chỉnh các file giao diện/logic (ví dụ `index.html`, `widget-loader.js`… tùy cấu trúc repo).
3. Deploy lên hosting của bạn (GitHub Pages, Vercel, Netlify, server riêng…).
4. Thay URL script loader từ domain của bạn.

> Lợi ích: kiểm soát phiên bản, cache, CSP, và tránh phụ thuộc vào đường dẫn public.

---

## Khắc phục sự cố

### Widget không hiển thị
- Kiểm tra bạn có chèn `<script src=".../widget-loader.js"></script>` chưa.
- Thử đặt script xuống cuối `<body>` để chắc chắn DOM đã sẵn sàng.

### Widget hiển thị “dữ liệu mẫu” / không tải được dữ liệu
Trong demo có tình huống “API Key hết hạn hoặc lỗi kết nối”. citeturn10view1  
Bạn nên:
- kiểm tra cấu hình API key (nếu widget yêu cầu),
- kiểm tra CORS / network,
- kiểm tra rate limit của nhà cung cấp thời tiết.

### Widget làm “vỡ layout”
- Bọc bằng container có `max-width`, `padding`
- Tránh đặt widget trong flex/grid quá chặt mà không có `min-width` hoặc `flex-wrap`.

---

## Bảo mật & lưu ý sản xuất

- Nếu widget dùng API key phía client: cân nhắc hạn chế domain/referrer trong dashboard nhà cung cấp API.
- Cân nhắc Content Security Policy (CSP) của website: cần cho phép load script từ `d4m-dev.github.io` (hoặc domain bạn self-host).
- Nếu dùng cache/CDN: đặt versioning cho script (querystring hoặc đường dẫn version) để tránh “cache cũ”.

---

## License

Xem phần License trong repository để biết điều khoản sử dụng và phân phối. citeturn1view0
