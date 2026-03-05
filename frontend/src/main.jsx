import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import LoginPage from './pages/LoginPage';
import { auth } from './services/auth';

function Root() {
  const [loggedIn, setLoggedIn] = useState(auth.isLoggedIn());

  useEffect(() => {
    // Handle OAuth callback
    if (window.location.pathname === '/auth/callback') {
      if (auth.handleCallback()) setLoggedIn(true);
    }
  }, []);

  if (!loggedIn) return <LoginPage onLogin={() => setLoggedIn(true)} />;
  return <App onLogout={() => { auth.logout(); setLoggedIn(false); }} />;
}

ReactDOM.createRoot(document.getElementById('root')).render(<React.StrictMode><Root /></React.StrictMode>);
