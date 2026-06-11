import React from 'react';
import ReactDOM from 'react-dom/client';
import { MusicProvider } from './contexts/MusicContext.jsx';
import App from './App.jsx';
import './styles.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <MusicProvider>
      <App />
    </MusicProvider>
  </React.StrictMode>,
);