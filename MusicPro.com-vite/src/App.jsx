import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import { useMusic } from './contexts/MusicContext.jsx';
import TrangChu from './pages/TrangChu.jsx';
import KhamPha from './pages/KhamPha.jsx';
import YeuThich from './pages/YeuThich.jsx';
import CaiDat from './pages/CaiDat.jsx';
import './styles.css';

const AppContent = () => {
  const { theme, setTheme } = useMusic();
  const [currentNav, setCurrentNav] = useState(0);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    
    // Update currentNav based on route
    switch(location.pathname) {
      case '/': setCurrentNav(0); break;
      case '/kham-pha': setCurrentNav(1); break;
      case '/yeu-thich': setCurrentNav(2); break;
      case '/cai-dat': setCurrentNav(3); break;
      default: setCurrentNav(0);
    }
  }, [theme, location]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  const handleNavClick = (index, path) => {
    setCurrentNav(index);
    navigate(path);
  };

  return (
    <>
      <div className="top-bar">
        <div className="logo"><i className="fa-brands fa-youtube"></i> Music Pro</div>
        <div className="flex-center" style={{ gap: '15px' }}>
          <button className="theme-toggle flex-center" onClick={toggleTheme}>
            <i className={`fa-solid ${theme === 'dark' ? 'fa-moon' : 'fa-sun'}`}></i>
          </button>
          <div className="avatar" style={{ width: '36px', height: '36px', borderRadius: '50%', overflow: 'hidden', border: '2px solid var(--border)' }}>
            <img src="https://ui-avatars.com/api/?name=User&background=2962ff&color=fff" style={{ width: '100%' }} alt="Avatar" />
          </div>
        </div>
      </div>

      <Routes>
        <Route path="/" element={<TrangChu />} />
        <Route path="/kham-pha" element={<KhamPha />} />
        <Route path="/yeu-thich" element={<YeuThich />} />
        <Route path="/cai-dat" element={<CaiDat />} />
      </Routes>

      <nav className="bottom-nav">
        <div className={`nav-link ${currentNav === 0 ? 'active' : ''}`} onClick={() => handleNavClick(0, '/')}>
          <i className="fa-solid fa-house"></i> <span>Trang chủ</span>
        </div>
        <div className={`nav-link ${currentNav === 1 ? 'active' : ''}`} onClick={() => handleNavClick(1, '/kham-pha')}>
          <i className="fa-solid fa-compass"></i> <span>Khám phá</span>
        </div>
        <div className={`nav-link ${currentNav === 2 ? 'active' : ''}`} onClick={() => handleNavClick(2, '/yeu-thich')}>
          <i className="fa-solid fa-heart"></i> <span>Yêu thích</span>
        </div>
        <div className={`nav-link ${currentNav === 3 ? 'active' : ''}`} onClick={() => handleNavClick(3, '/cai-dat')}>
          <i className="fa-solid fa-gear"></i> <span>Cài đặt</span>
        </div>
      </nav>
    </>
  );
};

const App = () => {
  return (
    <Router>
      <div className="app-layout">
        <AppContent />
      </div>
    </Router>
  );
};

export default App;