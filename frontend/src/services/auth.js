const API = 'http://localhost:8000';

export const auth = {
  async login(email, password) {
    const r = await fetch(`${API}/api/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) });
    if (!r.ok) throw new Error((await r.json()).detail || 'Giriş başarısız');
    const data = await r.json();
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  },
  async register(email, password, full_name, lang) {
    const r = await fetch(`${API}/api/auth/register`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password, full_name, lang }) });
    if (!r.ok) throw new Error((await r.json()).detail || 'Kayıt başarısız');
    const data = await r.json();
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  },
  loginWithLine() { window.location.href = `${API}/api/auth/line`; },
  loginWithFacebook() { window.location.href = `${API}/api/auth/facebook`; },
  loginWithGoogle() { window.location.href = `${API}/api/auth/google`; },
  handleCallback() {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');
    if (token) { localStorage.setItem('token', token); window.history.replaceState({}, '', '/'); return true; }
    return false;
  },
  getToken() { return localStorage.getItem('token'); },
  getUser() { try { return JSON.parse(localStorage.getItem('user')); } catch { return null; } },
  isLoggedIn() { return !!localStorage.getItem('token'); },
  logout() { localStorage.removeItem('token'); localStorage.removeItem('user'); },
};
