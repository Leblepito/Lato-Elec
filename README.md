# ⚡ ElectroPMS v5.0

**Otel Elektrik Bakım Yönetim Sistemi**
AntiGravity Ventures • Phuket, Thailand

---

## Hızlı Kurulum (3 Dakika)

### Gereksinimler

| Araç | Versiyon |
|------|----------|
| Docker + Docker Compose | ≥24.x |
| Node.js | ≥18.x (sadece lokal dev) |
| Python | ≥3.11 (sadece lokal dev) |

### 1-Komut Kurulum (Docker)

```bash
git clone https://github.com/antigravity-ventures/electropms.git
cd electropms
cp .env.example .env
# .env dosyasını düzenle (API key'leri gir)
docker compose up -d
```

Tamamlandığında:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Manuel Kurulum (Docker olmadan)

```bash
# 1. Database
createdb electropms
psql electropms < database/schema.sql

# 2. Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# 3. Frontend
cd frontend
npm install
npm run dev
```

---

## Proje Yapısı

```
electropms/
├── README.md                    ← Bu dosya
├── docker-compose.yml           ← Tek komut kurulum
├── .env.example                 ← Ortam değişkenleri şablonu
├── Makefile                     ← Kısayol komutlar
│
├── frontend/                    ← React + Vite + Capacitor
│   ├── package.json
│   ├── vite.config.js
│   ├── capacitor.config.ts
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx              ← Ana uygulama (13 modül)
│       ├── services/
│       │   ├── api.js           ← Backend HTTP client
│       │   ├── auth.js          ← Kimlik doğrulama
│       │   ├── camera.js        ← Kamera servisi
│       │   ├── geolocation.js   ← GPS + geofencing
│       │   └── push.js          ← Push notification
│       └── pages/
│           └── LoginPage.jsx    ← Giriş ekranı
│
├── backend/                     ← FastAPI + SQLAlchemy
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── app/
│   │   ├── main.py              ← FastAPI app + CORS + routes
│   │   ├── config.py            ← Ayarlar (.env okuma)
│   │   ├── database.py          ← DB bağlantı + session
│   │   ├── models/
│   │   │   ├── user.py          ← Kullanıcı modeli
│   │   │   ├── equipment.py     ← Ekipman modeli
│   │   │   ├── work_order.py    ← İş emri modeli
│   │   │   └── message.py       ← Mesaj modeli
│   │   ├── api/
│   │   │   ├── auth.py          ← Login/register/OAuth
│   │   │   ├── equipment.py     ← Ekipman CRUD
│   │   │   ├── work_orders.py   ← İş emri CRUD
│   │   │   ├── analysis.py      ← AI analiz (video/foto)
│   │   │   ├── messages.py      ← Mesajlaşma
│   │   │   └── staff.py         ← Personel + GPS
│   │   ├── services/
│   │   │   ├── ai_analysis.py   ← Claude API entegrasyonu
│   │   │   ├── line_service.py  ← LINE Messaging API
│   │   │   └── file_processor.py← Dosya format dönüştürme
│   │   ├── middleware/
│   │   │   └── auth.py          ← JWT + OAuth middleware
│   │   └── utils/
│   │       └── video_extractor.py ← yt-dlp wrapper
│   ├── migrations/              ← Alembic migrations
│   └── tests/
│
├── database/
│   ├── schema.sql               ← Tam DB şeması
│   ├── seed.sql                 ← Demo veri
│   └── indexes.sql              ← Performans indexleri
│
├── scripts/
│   ├── setup.sh                 ← Otomatik kurulum
│   ├── backup.sh                ← DB yedekleme
│   └── deploy.sh                ← Production deploy
│
└── docs/
    └── api.md                   ← API dokümantasyonu
```

---

## 13 Modül

| # | Modül | Açıklama |
|---|-------|----------|
| ⚡ | Dashboard | MDB canlı veriler, alarm, jeneratör, UPS, PFC |
| 🔌 | Panel SCADA | Pano ağaç şeması, sıcaklık haritası |
| 🌊 | Havuz Pompa | VFD kontrol, debi, basınç, izolasyon |
| 💧 | Tahliye | Sump seviye, lead/lag otomatik |
| 🏭 | MCC | Motor kontrol merkezi tablo |
| 🔧 | Bakım | PM takvimi (günlük→yıllık) |
| 📋 | İş Emri | Oluştur, takip et, tamamla |
| 🔒 | LOTO | 8 adım interaktif checklist |
| 🧮 | Hesaplama | Motor akım, MCCB, termik, kablo |
| 📎 | Dosya/AI | Her format yükle → Claude analiz |
| 🤖 | AI Analiz | Video/foto → 5 aksiyon butonu |
| 💬 | Mesajlaşma | LINE + uygulama içi + AI chat |
| 📍 | GPS | Geofencing + personel takip |

---

## Kimlik Doğrulama

| Yöntem | Açıklama |
|--------|----------|
| Email + Şifre | Standart kayıt/giriş |
| LINE Login | LINE OAuth 2.0 |
| Facebook Login | Facebook OAuth 2.0 |
| Google Login | Google OAuth 2.0 |

---

## Ortam Değişkenleri

`.env.example` dosyasını `.env` olarak kopyala ve doldur:

```
DATABASE_URL=postgresql://electropms:secret@localhost:5432/electropms
SECRET_KEY=your-256-bit-secret
ANTHROPIC_API_KEY=sk-ant-...
LINE_CHANNEL_ID=your-line-channel-id
LINE_CHANNEL_SECRET=your-line-channel-secret
FACEBOOK_APP_ID=your-fb-app-id
FACEBOOK_APP_SECRET=your-fb-secret
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-secret
```

---

## Lisans

Proprietary — AntiGravity Ventures © 2026
