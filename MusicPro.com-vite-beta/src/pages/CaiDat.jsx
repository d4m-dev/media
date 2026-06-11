import React, { useState } from 'react';

const CaiDat = () => {
  const [theme, setTheme] = useState('dark');
  const [volume, setVolume] = useState(0.8);
  const [notifications, setNotifications] = useState(true);
  const [autoPlay, setAutoPlay] = useState(true);

  const settingsSections = [
    {
      title: 'Giao diện',
      items: [
        { name: 'Chủ đề', desc: theme === 'dark' ? 'Tối' : 'Sáng', action: 'toggle', onClick: () => setTheme(theme === 'dark' ? 'light' : 'dark') },
        { name: 'Màu sắc chính', desc: 'Tùy chỉnh', action: 'color-picker' },
        { name: 'Phông chữ', desc: 'Urbanist', action: 'selector' },
        { name: 'Kiểu bố trí', desc: 'Tiêu chuẩn', action: 'layout-selector' }
      ]
    },
    {
      title: 'Tính năng',
      items: [
        { name: 'Tự động phát', desc: 'Tiếp tục phát khi mở lại', action: 'toggle', value: autoPlay, onToggle: () => setAutoPlay(!autoPlay) },
        { name: 'Thông báo', desc: 'Hiển thị thông báo hệ thống', action: 'toggle', value: notifications, onToggle: () => setNotifications(!notifications) },
        { name: 'Chế độ ngủ', desc: 'Tắt nhạc sau thời gian nhất định', action: 'timer' },
        { name: 'Tăng dần âm lượng', desc: 'Tăng dần âm lượng khi phát', action: 'toggle' }
      ]
    },
    {
      title: 'Bảo mật',
      items: [
        { name: 'Mã PIN', desc: 'Bảo vệ quyền truy cập', action: 'lock' },
        { name: 'Touch ID', desc: 'Mở khóa bằng vân tay', action: 'toggle' }
      ]
    },
    {
      title: 'Chung',
      items: [
        { name: 'Ngôn ngữ', desc: 'Tiếng Việt', action: 'language' },
        { name: 'Chất lượng âm thanh', desc: '320kbps', action: 'quality' },
        { name: 'Dữ liệu di động', desc: 'Quản lý sử dụng dữ liệu', action: 'data' },
        { name: 'Khôi phục cài đặt gốc', desc: 'Đặt lại tất cả cài đặt', action: 'reset' }
      ]
    }
  ];

  return (
    <div className="page-container">
      <div className="settings-container">
        {settingsSections.map((section, index) => (
          <div key={index} className="settings-section">
            <div className="settings-title">{section.title}</div>
            {section.items.map((item, idx) => (
              <div key={idx} className="settings-item" onClick={item.onClick || item.onToggle}>
                <div className="settings-icon">
                  <i className={`fa-solid ${getIconForSetting(item.name)}`}></i>
                </div>
                <div className="settings-info">
                  <div className="settings-name">{item.name}</div>
                  <div className="settings-desc">{item.desc}</div>
                </div>
                <div className="settings-action">
                  {item.action === 'toggle' ? (
                    <div className={`toggle-switch ${item.value ? 'active' : ''}`}>
                      <div className="toggle-handle"></div>
                    </div>
                  ) : item.action === 'color-picker' ? (
                    <div className="color-preview" style={{ width: '20px', height: '20px', backgroundColor: '#2962ff', borderRadius: '50%' }}></div>
                  ) : (
                    <span className="status-indicator status-info">{item.desc}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

// Helper function to get appropriate icon for settings
const getIconForSetting = (settingName) => {
  switch(settingName) {
    case 'Chủ đề': return 'fa-palette';
    case 'Màu sắc chính': return 'fa-swatchbook';
    case 'Phông chữ': return 'fa-font';
    case 'Kiểu bố trí': return 'fa-table-columns';
    case 'Tự động phát': return 'fa-play';
    case 'Thông báo': return 'fa-bell';
    case 'Chế độ ngủ': return 'fa-moon';
    case 'Tăng dần âm lượng': return 'fa-volume-up';
    case 'Mã PIN': return 'fa-lock';
    case 'Touch ID': return 'fa-fingerprint';
    case 'Ngôn ngữ': return 'fa-language';
    case 'Chất lượng âm thanh': return 'fa-headphones';
    case 'Dữ liệu di động': return 'fa-wifi';
    case 'Khôi phục cài đặt gốc': return 'fa-rotate-left';
    default: return 'fa-gear';
  }
};

export default CaiDat;