(function() {
    // 1. Xác định vị trí thẻ script đang chạy
    var scriptElement = document.currentScript || (function() {
        var scripts = document.getElementsByTagName('script');
        return scripts[scripts.length - 1];
    })();

    // 2. CẤU HÌNH ĐƯỜNG DẪN MẶC ĐỊNH
    // Đây là link đến trang widget của bạn trên GitHub
    var defaultUrl = 'https://d4m-dev.github.io/WidgetWeather.com/'; 
    
    // Lấy link từ thuộc tính data-source, nếu không có thì dùng link mặc định ở trên
    var widgetUrl = scriptElement.getAttribute('data-source') || defaultUrl;

    // 3. CSS tạo khung và Responsive
    var css = `
        .weather-widget-wrapper {
            width: 100%;
            max-width: 600px; /* Độ rộng tối đa trên PC */
            margin: 20px auto;
            overflow: hidden;
            border-radius: 20px;
            position: relative;
            z-index: 1;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            background: transparent;
        }
        .weather-widget-frame {
            width: 100%;
            border: none;
            display: block;
            height: 500px; /* Chiều cao mặc định PC */
            transition: height 0.3s ease;
            background: transparent;
        }
        /* Mobile: Tự động cao lên để hiện đủ danh sách dọc */
        @media (max-width: 768px) {
            .weather-widget-wrapper {
                max-width: 100%;
                margin: 10px 0;
                border-radius: 12px;
            }
            .weather-widget-frame {
                height: 900px; /* Tăng chiều cao cho giao diện mobile dọc */
            }
        }
    `;
    
    // Chèn CSS vào đầu trang
    var style = document.createElement('style');
    style.type = 'text/css';
    if (style.styleSheet){
        style.styleSheet.cssText = css;
    } else {
        style.appendChild(document.createTextNode(css));
    }
    document.head.appendChild(style);

    // 4. Tạo Iframe chứa Widget
    var wrapper = document.createElement('div');
    wrapper.className = 'weather-widget-wrapper';

    var iframe = document.createElement('iframe');
    iframe.className = 'weather-widget-frame';
    iframe.src = widgetUrl;
    iframe.title = "Dự báo thời tiết";
    iframe.setAttribute('allow', 'geolocation'); 
    iframe.setAttribute('loading', 'lazy');     

    wrapper.appendChild(iframe);

    // 5. Chèn vào trang web
    scriptElement.parentNode.insertBefore(wrapper, scriptElement.nextSibling);

})();