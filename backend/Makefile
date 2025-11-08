.PHONY: help build up down restart logs shell migrate makemigrations createsuperuser collectstatic clean test

# ============================================
# Help
# ============================================
help: ## Show this help message
	@echo "📋 Passd Backend - Docker Commands"
	@echo "===================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ============================================
# Docker Operations
# ============================================
build: ## Build Docker images
	@echo "🔨 Building Docker images..."
	docker-compose build

up: ## Start all services
	@echo "🚀 Starting services..."
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "🌐 Backend available at: http://localhost:8000"

down: ## Stop all services
	@echo "🛑 Stopping services..."
	docker-compose down
	@echo "✅ Services stopped!"

restart: ## Restart all services
	@echo "🔄 Restarting services..."
	docker-compose restart
	@echo "✅ Services restarted!"

logs: ## Show logs (use make logs service=backend for specific service)
	@if [ -z "$(service)" ]; then \
		docker-compose logs -f; \
	else \
		docker-compose logs -f $(service); \
	fi

logs-backend: ## Show backend logs
	docker-compose logs -f backend

logs-db: ## Show database logs
	docker-compose logs -f db

# ============================================
# Django Operations
# ============================================
shell: ## Open Django shell
	docker-compose exec backend python manage.py shell

shell-bash: ## Open bash shell in backend container
	docker-compose exec backend bash

migrate: ## Run database migrations
	@echo "📦 Running migrations..."
	docker-compose exec backend python manage.py migrate

makemigrations: ## Create new migrations
	@echo "📝 Creating migrations..."
	docker-compose exec backend python manage.py makemigrations

createsuperuser: ## Create Django superuser
	@echo "👤 Creating superuser..."
	docker-compose exec backend python manage.py createsuperuser

seed-data: ## Create test data (users, folders, items)
	@echo "🌱 Creating test data..."
	docker-compose exec backend python manage.py seed_data
	@echo "✅ Test data created!"

seed-data-clear: ## Clear and recreate all test data (WARNING: deletes all data)
	@echo "⚠️  WARNING: This will delete ALL existing data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose exec backend python manage.py seed_data --clear; \
		echo "✅ Test data recreated!"; \
	else \
		echo "❌ Cancelled."; \
	fi

collectstatic: ## Collect static files
	@echo "📁 Collecting static files..."
	docker-compose exec backend python manage.py collectstatic --noinput

# ============================================
# Database Operations
# ============================================
db-shell: ## Open PostgreSQL shell
	docker-compose exec db psql -U passd_user -d passd_db

db-backup: ## Backup database
	@echo "💾 Backing up database..."
	docker-compose exec -T db pg_dump -U passd_user passd_db > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup created!"

db-restore: ## Restore database (use make db-restore file=backup.sql)
	@if [ -z "$(file)" ]; then \
		echo "❌ Please specify backup file: make db-restore file=backup.sql"; \
	else \
		echo "📥 Restoring database from $(file)..."; \
		docker-compose exec -T db psql -U passd_user -d passd_db < $(file); \
		echo "✅ Database restored!"; \
	fi

# ============================================
# Development
# ============================================
dev: ## Start development environment (with logs)
	@echo "🔧 Starting development environment..."
	docker-compose up

dev-build: ## Rebuild and start development environment
	@echo "🔨 Rebuilding and starting..."
	docker-compose up --build

test: ## Run tests
	@echo "🧪 Running tests..."
	docker-compose exec backend python manage.py test

# ============================================
# Cleanup
# ============================================
clean: ## Remove all containers, volumes, and images
	@echo "🧹 Cleaning up..."
	docker-compose down -v --remove-orphans
	@echo "✅ Cleanup complete!"

clean-all: ## Remove everything including images
	@echo "🧹 Deep cleaning..."
	docker-compose down -v --rmi all --remove-orphans
	@echo "✅ Deep cleanup complete!"

# ============================================
# Setup
# ============================================
setup: ## Initial setup (build, up, migrate)
	@echo "🎯 Setting up Passd Backend..."
	@if [ ! -f .env ]; then \
		echo "📝 Creating .env file from .env.example..."; \
		cp .env.example .env; \
		echo "⚠️  Please update .env with your configuration!"; \
	fi
	@echo "🔨 Building images..."
	docker-compose build
	@echo "🚀 Starting services..."
	docker-compose up -d
	@echo "⏳ Waiting for services to be ready..."
	sleep 10
	@echo "📦 Running migrations..."
	docker-compose exec backend python manage.py migrate
	@echo "✅ Setup complete!"
	@echo "🌐 Backend available at: http://localhost:8000"
	@echo "📊 Admin panel: http://localhost:8000/admin/"

# ============================================
# Status
# ============================================
status: ## Show status of all services
	@echo "📊 Service Status:"
	@docker-compose ps

ps: status ## Alias for status
