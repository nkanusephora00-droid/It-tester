# Docker Configuration

This directory contains Docker configuration files to run the IT Access Manager application.

## Services

- **Backend**: FastAPI application running on port 8000
- **Frontend**: React application served with Nginx on port 3000
- **Database**: PostgreSQL 15 on port 5432

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Navigate to the docker directory:
   ```bash
   cd docker
   ```

2. Build and start all services:
   ```bash
   docker-compose up -d
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Database: localhost:5432

## Commands

### Start services
```bash
docker-compose up -d
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Stop services
```bash
docker-compose down
```

### Rebuild services
```bash
docker-compose build --no-cache
```

### Remove volumes (data will be lost)
```bash
docker-compose down -v
```

## Environment Variables

The following environment variables are used:

- `DATABASE_URL`: PostgreSQL connection string
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name

## Notes

- The frontend is configured to proxy API requests to the backend through Nginx
- Database data is persisted in a Docker volume
- The containers restart automatically unless stopped
