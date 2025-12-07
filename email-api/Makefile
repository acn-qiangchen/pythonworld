.PHONY: help build run stop logs test clean install dev

# Default target
help:
	@echo "Email API - Available Commands"
	@echo "================================"
	@echo "make build       - Build Docker image"
	@echo "make run         - Run container with docker-compose"
	@echo "make stop        - Stop and remove containers"
	@echo "make logs        - View container logs"
	@echo "make test        - Run API tests"
	@echo "make clean       - Remove containers and images"
	@echo "make install     - Install Python dependencies locally"
	@echo "make dev         - Run locally for development"
	@echo ""

# Build Docker image
build:
	@echo "Building Docker image..."
	docker build -t email-api:latest .
	@echo "✓ Build complete!"

# Run with docker-compose
run:
	@echo "Starting Email API service..."
	docker-compose up -d
	@echo "✓ Service started!"
	@echo "API available at: http://localhost:8000"
	@echo "Docs available at: http://localhost:8000/docs"

# Stop containers
stop:
	@echo "Stopping Email API service..."
	docker-compose down
	@echo "✓ Service stopped!"

# View logs
logs:
	docker-compose logs -f

# Run tests
test:
	@echo "Running API tests..."
	@echo "Make sure the API is running first (make run)"
	python test_api.py

# Clean up
clean:
	@echo "Cleaning up containers and images..."
	docker-compose down
	docker rmi email-api:latest || true
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
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

