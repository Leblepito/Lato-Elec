# การมีส่วนร่วม / Katkıda Bulunma

## Geliştirme Ortamı / สภาพแวดล้อมการพัฒนา

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## Branch Kuralları / กฎ Branch

| Branch | Amaç |
|--------|------|
| `main` | Production — sadece PR ile |
| `fix/*` | Bug fix |
| `feat/*` | Yeni özellik |
| `docs/*` | Dokümantasyon |

## Commit Formatı

```
type: kısa açıklama

fix: backend CORS hatası düzeltildi
feat: LINE webhook entegrasyonu
docs: README güncellendi
```

## PR Checklist

- [ ] Backend çalışıyor: `uvicorn app.main:app`
- [ ] Frontend çalışıyor: `npm run dev`
- [ ] Yeni endpoint varsa → README'ye ekle
- [ ] Yeni model varsa → schema.sql güncelle
