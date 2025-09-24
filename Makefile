.PHONY: help dev prod build test migrate shell clean

help:  ## Display this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

dev:  ## Start development server in dev container
	python manage.py runserver 0.0.0.0:8001

makemigrations:  ## Create new migrations (run manually when models change)
	python manage.py makemigrations

migrate:  ## Run database migrations
	python manage.py migrate

shell:  ## Open Django shell
	python manage.py shell

test:  ## Run tests
	python manage.py test

superuser:  ## Create superuser
	python manage.py createsuperuser

collectstatic:  ## Collect static files
	python manage.py collectstatic --noinput

build-dev:  ## Build development Docker image
	docker build -f Dockerfile.dev -t django-app-dev .

build-prod:  ## Build production Docker image
	docker build -f Dockerfile -t django-app-prod .

prod-up:  ## Start production environment with docker-compose
	docker-compose -f docker-compose.prod.yml up -d

prod-down:  ## Stop production environment
	docker-compose -f docker-compose.prod.yml down

prod-logs:  ## View production logs
	docker-compose -f docker-compose.prod.yml logs -f

clean:  ## Clean up Docker containers and images
	docker system prune -f

lint:  ## Run code linting
	flake8 .
	black --check .
	isort --check-only .

format:  ## Format code with black and isort
	black .
	isort .