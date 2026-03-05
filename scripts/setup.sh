#!/bin/bash
# ═══════════════════════════════════════════
# ElectroPMS v6 — Otomatik Kurulum / สคริปต์ติดตั้ง
# ═══════════════════════════════════════════
set -e

echo "⚡ ElectroPMS v6 — Kurulum / ติดตั้ง..."

if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 .env oluşturuldu — API key'leri doldur! / สร้าง .env แล้ว กรอก API key!"
fi

if command -v docker &> /dev/null; then
    echo "🐳 Docker bulundu / พบ Docker..."
    docker compose up -d --build
    echo ""
    echo "✅ Tamamlandı / เสร็จสิ้น!"
    echo "   Frontend:  http://localhost:5173"
    echo "   Backend:   http://localhost:8000"
    echo "   Swagger:   http://localhost:8000/docs"
    echo "   Demo:      utku@antigravity.com / demo123"
else
    echo "⚠️  Docker yok / ไม่พบ Docker — manuel kurulum..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate 2>/dev/null || . venv/Scripts/activate
    pip install -r requirements.txt
    cd ..
    cd frontend && npm install && cd ..
    if command -v psql &> /dev/null; then
        createdb electropms 2>/dev/null || true
        psql electropms < database/schema.sql
        psql electropms < database/seed.sql
        psql electropms < database/indexes.sql
    fi
    echo ""
    echo "✅ Başlatmak için / เพื่อเริ่ม:"
    echo "   Backend:  cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
    echo "   Frontend: cd frontend && npm run dev"
fi
