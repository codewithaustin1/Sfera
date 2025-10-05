Overview
Refactored parsing services for the Sfera Information System, migrated to Python with standardized corporate structure following SMK-RK requirements.

Project Structure

sfera-refactored/
├── api/v1/                 # API versioning
├── controllers/            # HTTP controllers
├── core/                   # Configuration and constants
├── domain/                 # Business logic (DDD)
│   ├── models/            # Data models
│   ├── interfaces/        # Abstract interfaces
│   └── services/          # Business services
├── infrastructure/         # External integrations
├── docker-compose.yml     # Development Docker setup
├── docker-compose-prod.yml # Production Docker setup
├── Dockerfile-dev         # Development Dockerfile
├── Dockerfile-prod        # Production Dockerfile
└── main.py               # Application entry point

Quick Start

Prerequisites
Python 3.11+

Docker & Docker Compose

Local Development

# Clone and setup
git clone <repository>
cd sfera-refactored

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn infrastructure.main:app --reload --port 8000


Docker Development

# Start with Docker Compose
docker-compose up -d

# Check services
docker-compose ps

Production Deployment

# Production deployment
docker-compose -f docker-compose-prod.yml up -d


