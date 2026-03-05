# Changelog

## v6.0.0 — 2026-03-06

### เพิ่ม / Eklenen
- Backend: Equipment, WorkOrder, Message SQLAlchemy modelleri
- Backend: Equipment CRUD + `/tree` + `/readings/bulk` (IoT gateway girişi)
- Backend: WorkOrder CRUD + otomatik WO-ID + durum geçişleri
- Backend: Messages API + LINE webhook endpoint
- Backend: AI Analysis — Claude Vision fotoğraf + yt-dlp video URL
- Frontend: PWA manifest — telefona kurulabilir
- Frontend: Tam Tayca çeviri (80+ terim)
- Frontend: Dosya yükleme (drag&drop, kamera, galeri — tüm formatlar)
- Frontend: LINE + uygulama içi mesajlaşma
- Frontend: Panel SCADA ağaç görünümü
- Deploy: Railway config (backend + frontend toml)
- Docs: CONTRIBUTING.md, CHANGELOG.md

### แก้ไข / Düzeltilen
- Backend placeholder endpoint'ler → gerçek DB sorguları
- README repo URL ve dosya ağacı düzeltildi
- Makefile'dan olmayan alembic komutu kaldırıldı
- .env.example temizlendi (kullanılmayan Firebase kaldırıldı)

## v5.0.0 — 2026-03-06

### เพิ่ม / Eklenen
- İlk commit: Frontend + Backend + Database + Docker
- Auth: JWT + LINE/Facebook/Google OAuth
- 13 tablo PostgreSQL şeması
- Demo seed data (4 kullanıcı, ekipman hiyerarşisi)
