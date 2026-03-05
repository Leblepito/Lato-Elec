# ⚡ ElectroPMS v6.0

**ระบบจัดการไฟฟ้าโรงแรม — Otel Elektrik Bakım Yönetim Sistemi**
AntiGravity Ventures • Phuket, Thailand

---

## ติดตั้ง / Kurulum

### Railway (แนะนำ / Önerilen)

1. [railway.app](https://railway.app) → New Project
2. **PostgreSQL** → Database → PostgreSQL ekle
3. **Backend** → GitHub Repo → `Leblepito/Lato-Elec` → Root: `backend`
4. **Frontend** → GitHub Repo → `Leblepito/Lato-Elec` → Root: `frontend`
5. Backend Variables:
   ```
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   SECRET_KEY=rastgele-256-bit
   ANTHROPIC_API_KEY=sk-ant-...
   ```

### Docker

```bash
git clone https://github.com/Leblepito/Lato-Elec.git
cd Lato-Elec
cp .env.example .env
docker compose up -d
```

| Servis | URL |
|--------|-----|
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |

### Demo: `utku@antigravity.com` / `demo123`

---

## โครงสร้าง / Yapı

```
Lato-Elec/
├── README.md
├── .env.example
├── .gitignore
├── Makefile
├── docker-compose.yml
├── railway.json
│
├── backend/
│   ├── Dockerfile
│   ├── railway.toml
│   ├── requirements.txt
│   └── app/
│       ├── main.py              # 5 router
│       ├── config.py
│       ├── database.py
│       ├── api/
│       │   ├── auth.py          # JWT + OAuth (LINE/FB/Google)
│       │   ├── equipment.py     # CRUD + /tree + /readings/bulk
│       │   ├── work_orders.py   # CRUD + auto ID
│       │   ├── messages.py      # LINE + app + webhook
│       │   └── analysis.py      # Claude Vision + yt-dlp
│       ├── models/
│       │   ├── user.py
│       │   ├── equipment.py
│       │   ├── work_order.py
│       │   └── message.py
│       └── middleware/
│           └── auth.py          # JWT verify
│
├── frontend/
│   ├── Dockerfile
│   ├── railway.toml
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   ├── public/manifest.json     # PWA
│   └── src/
│       ├── main.jsx
│       ├── App.jsx              # 11 modül + login
│       ├── pages/LoginPage.jsx
│       └── services/auth.js
│
├── database/
│   ├── schema.sql               # 13 tablo
│   ├── seed.sql                 # Demo veri
│   └── indexes.sql
│
└── scripts/setup.sh
```

---

## โมดูล / Modüller

| | TH | TR |
|--|----|----|
| ⚡ | หน้าหลัก | Dashboard — MDB, alarm, UPS, PFC |
| 🔌 | ตู้ไฟ SCADA | Panel — ağaç şeması, sıcaklık |
| 🌊 | สระน้ำ | Havuz — VFD, debi, basınç |
| 💧 | ระบาย | Tahliye — sump, lead/lag |
| 🏭 | MCC | Motor kontrol merkezi |
| 📋 | คำสั่งงาน | İş Emri — CRUD |
| 🔒 | LOTO | 8 adım güvenlik checklist |
| 🧮 | คำนวณ | Hesaplama — akım, MCCB, kablo |
| 📎 | ไฟล์+AI | Dosya yükle → Claude analiz |
| 💬 | ข้อความ | Mesaj — LINE + app + AI |
| 📍 | GPS | Geofencing + konum takip |

---

## API

```
GET  /api/health
POST /api/auth/register          # Email kayıt
POST /api/auth/login             # Email → JWT
GET  /api/auth/line              # LINE OAuth
GET  /api/auth/facebook          # Facebook OAuth
GET  /api/auth/google            # Google OAuth
GET  /api/equipment/             # Liste
GET  /api/equipment/tree         # Pano hiyerarşi
POST /api/equipment/readings/bulk # Gateway veri
GET  /api/workorders/            # İş emri liste
POST /api/workorders/            # Yeni iş emri
POST /api/workorders/{id}/complete
GET  /api/messages/              # Mesajlar
POST /api/messages/              # Mesaj gönder
POST /api/messages/line-webhook  # LINE webhook
POST /api/analyze/url            # Video → AI
POST /api/analyze/photo          # Fotoğraf → AI
```

---

## การยืนยันตัวตน / Auth

| | Yöntem |
|--|--------|
| ✉️ | Email + Şifre (JWT) |
| 💚 | LINE OAuth 2.0 |
| 📘 | Facebook OAuth 2.0 |
| 🔍 | Google OAuth 2.0 |
| 🚀 | Demo (backend gerektirmez) |

---

## ตัวแปร / Env

| Key | Açıklama |
|-----|----------|
| `DATABASE_URL` | PostgreSQL |
| `SECRET_KEY` | JWT 256-bit |
| `ANTHROPIC_API_KEY` | Claude AI |
| `LINE_CHANNEL_ID` | LINE OAuth |
| `LINE_CHANNEL_SECRET` | LINE OAuth |
| `FACEBOOK_APP_ID` | FB OAuth |
| `GOOGLE_CLIENT_ID` | Google OAuth |

---

## เทคโนโลยี / Stack

Frontend: React 18 + Vite + PWA
Backend: FastAPI + SQLAlchemy
Database: PostgreSQL 16 (13 tablo)
AI: Claude Sonnet 4 + yt-dlp
Auth: JWT + OAuth 2.0
Messaging: LINE API
Deploy: Railway / Docker
Mobile: PWA (QR → telefona ekle)

---

**AntiGravity Ventures © 2026 • Phuket, Thailand**
