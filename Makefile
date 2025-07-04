.PHONY: help install test lint format clean build docker-build docker-run deploy

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install all dependencies"
	@echo "  test        - Run all tests"
	@echo "  lint        - Run linting checks"
	@echo "  format      - Format code"
	@echo "  clean       - Clean build artifacts"
	@echo "  build       - Build the application"
	@echo "  docker-run  - Run with Docker Compose (optional)"
	@echo "  deploy      - Deploy to production"

# Install dependencies
install:
	@echo "Installing Python dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing Node.js dependencies..."
	cd frontend && npm install
	@echo "Installing pre-commit hooks..."
	pre-commit install

# Run tests
test:
	@echo "Running backend tests..."
	cd backend && pytest --cov=app --cov-report=term-missing
	@echo "Running frontend tests..."
	cd frontend && npm test -- --coverage --watchAll=false

# Run linting
lint:
	@echo "Linting Python code..."
	cd backend && flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
	cd backend && flake8 app/ --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics
	@echo "Linting JavaScript code..."
	cd frontend && npm run lint

# Format code
format:
	@echo "Formatting Python code..."
	cd backend && black app/
	cd backend && isort app/
	@echo "Formatting JavaScript code..."
	cd frontend && npm run format

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	cd frontend && rm -rf build/ node_modules/

# Build the application
build:
	@echo "Building frontend..."
	cd frontend && npm run build
	@echo "Build complete!"

# Build Docker images (optional for local development)
docker-build:
	@echo "Building Docker images..."
	cd backend && docker build -t vul-detector-backend .
	cd frontend && docker build -t vul-detector-frontend .

# Run with Docker Compose
docker-run:
	@echo "Starting services with Docker Compose..."
	docker-compose up --build

# Deploy to production
deploy:
	@echo "Deploying to production..."
	git push origin main

# Security scan
security:
	@echo "Running security scans..."
	cd backend && bandit -r app/
	cd backend && safety check

# Development setup
dev-setup: install
	@echo "Setting up development environment..."
	pre-commit install
	@echo "Development setup complete!"

# Quick start
quick-start: install
	@echo "Starting development servers..."
	@echo "Backend will be available at http://localhost:8000"
	@echo "Frontend will be available at http://localhost:3000"
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
	cd frontend && npm start 