import { useState } from 'react';
import { auth } from '../services/auth';

const S = {
  page: { minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: '#080c14', padding: 20 },
  card: { width: '100%', maxWidth: 380, background: '#0e1525', border: '1px solid #1a2540', borderRadius: 16, padding: 28, boxSizing: 'border-box' },
  logo: { textAlign: 'center', marginBottom: 24 },
  logoIcon: { fontSize: 48, marginBottom: 8 },
  logoTitle: { fontSize: 22, fontWeight: 800, color: '#dde4f0', letterSpacing: 1 },
  logoSub: { fontSize: 11, color: '#506080', marginTop: 4 },
  inp: { width: '100%', boxSizing: 'border-box', background: '#080c14', border: '1px solid #1a2540', borderRadius: 10, padding: '12px 14px', color: '#dde4f0', fontSize: 14, fontFamily: 'inherit', marginBottom: 10 },
  btn: (bg, color) => ({ width: '100%', padding: '13px', borderRadius: 10, border: 'none', fontSize: 14, fontWeight: 600, fontFamily: 'inherit', cursor: 'pointer', color: color || '#fff', background: bg, marginBottom: 8, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10, minHeight: 48 }),
  divider: { display: 'flex', alignItems: 'center', gap: 10, margin: '16px 0', color: '#506080', fontSize: 11 },
  line: { flex: 1, height: 1, background: '#1a2540' },
  err: { background: '#dc262615', border: '1px solid #dc262630', borderRadius: 8, padding: '8px 12px', fontSize: 12, color: '#fca5a5', marginBottom: 12 },
  switch: { textAlign: 'center', fontSize: 12, color: '#506080', marginTop: 12, cursor: 'pointer' },
  switchLink: { color: '#5b9bf5', fontWeight: 600 },
  lang: { display: 'flex', justifyContent: 'center', gap: 8, marginBottom: 16 },
  langBtn: (a) => ({ padding: '6px 14px', borderRadius: 8, border: a ? '1px solid #2563eb' : '1px solid #1a2540', background: a ? '#2563eb30' : 'transparent', color: a ? '#5b9bf5' : '#506080', cursor: 'pointer', fontSize: 12, fontWeight: 600, fontFamily: 'inherit' }),
};

export default function LoginPage({ onLogin }) {
  const [mode, setMode] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [lang, setLang] = useState('tr');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const L = lang === 'tr';

  const handleSubmit = async () => {
    setError(''); setLoading(true);
    try {
      if (mode === 'register') {
        await auth.register(email, password, name, lang);
      } else {
        await auth.login(email, password);
      }
      onLogin();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  // Demo login
  const demoLogin = () => {
    localStorage.setItem('token', 'demo-token');
    localStorage.setItem('user', JSON.stringify({ id: 'demo', email: 'utku@antigravity.com', full_name: 'Utku (Demo)', role: 'admin', lang }));
    onLogin();
  };

  return (
    <div style={S.page}>
      <div style={S.card}>
        <div style={S.logo}>
          <div style={S.logoIcon}>⚡</div>
          <div style={S.logoTitle}>ElectroPMS</div>
          <div style={S.logoSub}>Hotel Electrical Management • Phuket</div>
        </div>

        <div style={S.lang}>
          <button style={S.langBtn(lang === 'tr')} onClick={() => setLang('tr')}>🇹🇷 Türkçe</button>
          <button style={S.langBtn(lang === 'th')} onClick={() => setLang('th')}>🇹🇭 ไทย</button>
          <button style={S.langBtn(lang === 'en')} onClick={() => setLang('en')}>🇬🇧 EN</button>
        </div>

        {error && <div style={S.err}>❌ {error}</div>}

        {mode === 'register' && (
          <input style={S.inp} placeholder={L ? 'Ad Soyad' : 'ชื่อ-นามสกุล'} value={name} onChange={e => setName(e.target.value)} />
        )}
        <input style={S.inp} placeholder="Email" type="email" value={email} onChange={e => setEmail(e.target.value)} />
        <input style={S.inp} placeholder={L ? 'Şifre' : 'รหัสผ่าน'} type="password" value={password} onChange={e => setPassword(e.target.value)} onKeyDown={e => e.key === 'Enter' && handleSubmit()} />

        <button style={S.btn('#2563eb')} onClick={handleSubmit} disabled={loading}>
          {loading ? '⏳' : '⚡'} {mode === 'register' ? (L ? 'Kayıt Ol' : 'สมัครสมาชิก') : (L ? 'Giriş Yap' : 'เข้าสู่ระบบ')}
        </button>

        <div style={S.divider}><div style={S.line}></div><span>{L ? 'veya' : 'หรือ'}</span><div style={S.line}></div></div>

        <button style={S.btn('#06C755')} onClick={() => auth.loginWithLine()}>
          💚 LINE {L ? 'ile Giriş' : 'เข้าสู่ระบบ'}
        </button>
        <button style={S.btn('#1877F2')} onClick={() => auth.loginWithFacebook()}>
          📘 Facebook {L ? 'ile Giriş' : 'เข้าสู่ระบบ'}
        </button>
        <button style={S.btn('#1a2540', '#dde4f0')} onClick={() => auth.loginWithGoogle()}>
          🔍 Google {L ? 'ile Giriş' : 'เข้าสู่ระบบ'}
        </button>

        <div style={S.divider}><div style={S.line}></div><div style={S.line}></div></div>

        <button style={S.btn('#7c3aed')} onClick={demoLogin}>
          🚀 Demo {L ? 'Giriş (Backend gerektirmez)' : 'เข้าสู่ระบบ (ไม่ต้องใช้ backend)'}
        </button>

        <div style={S.switch} onClick={() => setMode(mode === 'login' ? 'register' : 'login')}>
          {mode === 'login' ? (L ? 'Hesabın yok mu? ' : 'ยังไม่มีบัญชี? ') : (L ? 'Zaten hesabın var mı? ' : 'มีบัญชีแล้ว? ')}
          <span style={S.switchLink}>{mode === 'login' ? (L ? 'Kayıt Ol' : 'สมัคร') : (L ? 'Giriş Yap' : 'เข้าสู่ระบบ')}</span>
        </div>
      </div>

      <div style={{ marginTop: 20, fontSize: 10, color: '#506080', textAlign: 'center' }}>
        AntiGravity Ventures © 2026 • Phuket, Thailand
      </div>
    </div>
  );
}
