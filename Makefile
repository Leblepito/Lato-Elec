.PHONY: up down build logs db-shell seed backup clean dev-backend dev-frontend

# Docker
up:
	docker compose up -d
down:
	docker compose down
build:
	docker compose build --no-cache
logs:
	docker compose logs -f

# Database
db-shell:
	docker compose exec postgres psql -U electropms -d electropms
db-init:
	docker compose exec postgres psql -U electropms -d electropms -f /docker-entrypoint-initdb.d/01-schema.sql
seed:
	docker compose exec postgres psql -U electropms -d electropms -f /docker-entrypoint-initdb.d/02-seed.sql
backup:
	docker compose exec postgres pg_dump -U electropms electropms > backup_$$(date +%Y%m%d_%H%M%S).sql

# Lokal geliştirme (Docker olmadan)
dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8000
dev-frontend:
	cd frontend && npm run dev

# Temizlik
clean:
	docker compose down -v --remove-orphans
