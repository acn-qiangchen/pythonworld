.PHONY: help build run stop logs test clean install dev migrate shell

# Default target
help:
	@echo "Django Email API - Available Commands"
	@echo "======================================"
	@echo "make build       - Build Docker image"
	@echo "make run         - Run container with docker-compose"
	@echo "make stop        - Stop and remove containers"
	@echo "make logs        - View container logs"
	@echo "make test        - Run Django tests"
	@echo "make clean       - Remove containers and images"
	@echo "make install     - Install Python dependencies locally"
	@echo "make dev         - Run locally for development"
	@echo "make migrate     - Run Django migrations"
	@echo "make shell       - Open Django shell"
	@echo ""

# Build Docker image
build:
	@echo "Building Docker image..."
	docker build -t email-api-django:latest .
	@echo "✓ Build complete!"

# Run with docker-compose
run:
	@echo "Starting Django Email API service..."
	docker-compose up -d
	@echo "✓ Service started!"
	@echo "API available at: http://localhost:8000/api/"
	@echo "Admin available at: http://localhost:8000/admin/"
	@echo "Browsable API: http://localhost:8000/api/v1/send-email/"

# Stop containers
stop:
	@echo "Stopping Django Email API service..."
	docker-compose down
	@echo "✓ Service stopped!"

# View logs
logs:
	docker-compose logs -f

# Run tests
test:
	@echo "Running Django tests..."
	python manage.py test

# Clean up
clean:
	@echo "Cleaning up containers and images..."
	docker-compose down
	docker rmi email-api-django:latest || true
	@echo "✓ Cleanup complete!"

# Install dependencies locally
install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✓ Dependencies installed!"

# Run locally for development
dev:
	@echo "Starting development server..."
	@echo "Make sure environment variables are set!"
	python manage.py runserver 0.0.0.0:8000

# Run migrations
migrate:
	@echo "Running Django migrations..."
	python manage.py migrate
	@echo "✓ Migrations complete!"

# Open Django shell
shell:
	python manage.py shell



