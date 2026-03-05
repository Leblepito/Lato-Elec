#!/bin/bash
# ═══════════════════════════════════════════
# ElectroPMS — Otomatik Kurulum Scripti
# ═══════════════════════════════════════════
set -e

echo "⚡ ElectroPMS v5 Kurulum Başlıyor..."

# 1. Env dosyası kontrol
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 .env dosyası oluşturuldu — lütfen API key'leri doldurun!"
fi

# 2. Docker kontrol
if command -v docker &> /dev/null; then
    echo "🐳 Docker bulundu — Docker ile kuruluyor..."
    docker compose up -d --build
    echo ""
    echo "✅ Kurulum tamamlandı!"
    echo "   Frontend:  http://localhost:5173"
    echo "   Backend:   http://localhost:8000"
    echo "   API Docs:  http://localhost:8000/docs"
    echo "   Demo giriş: utku@antigravity.com / demo123"
else
    echo "⚠️  Docker bulunamadı — manuel kurulum yapılıyor..."

    # Backend
    echo "📦 Backend kuruluyor..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate 2>/dev/null || . venv/Scripts/activate
    pip install -r requirements.txt
    cd ..

    # Frontend
    echo "📦 Frontend kuruluyor..."
    cd frontend
    npm install
    cd ..

    # DB
    if command -v psql &> /dev/null; then
        echo "🗄️  Database kuruluyor..."
        createdb electropms 2>/dev/null || true
        psql electropms < database/schema.sql
        psql electropms < database/seed.sql
        psql electropms < database/indexes.sql
    else
        echo "⚠️  PostgreSQL bulunamadı — database'i manuel kurun"
    fi

    echo ""
    echo "✅ Kurulum tamamlandı! Başlatmak için:"
    echo "   Backend:  cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
    echo "   Frontend: cd frontend && npm run dev"
fi
