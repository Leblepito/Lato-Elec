.PHONY: up down build logs db-shell api-shell seed migrate backup

# Hızlı başlat
up:
	docker compose up -d

# Durdur
down:
	docker compose down

# Yeniden build
build:
	docker compose build --no-cache

# Logları izle
logs:
	docker compose logs -f

# DB shell
db-shell:
	docker compose exec postgres psql -U electropms -d electropms

# API shell
api-shell:
	docker compose exec backend python -c "from app.database import get_db; print('DB OK')"

# Demo veri yükle
seed:
	docker compose exec postgres psql -U electropms -d electropms -f /docker-entrypoint-initdb.d/02-seed.sql

# Migration çalıştır
migrate:
	docker compose exec backend alembic upgrade head

# DB yedekle
backup:
	docker compose exec postgres pg_dump -U electropms electropms > backup_$$(date +%Y%m%d_%H%M%S).sql

# Temizlik
clean:
	docker compose down -v --remove-orphans
