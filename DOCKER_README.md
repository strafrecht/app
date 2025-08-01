# 🐳 Strafrecht Online - Docker Setup

Containerized deployment of the Strafrecht Online Wagtail Django application.

## ⚡ Quick Start

```bash
# 1. Setup environment
./docker/manage.sh setup dev

# 2. Start services
./docker/manage.sh up

# 3. Initialize application
./docker/manage.sh migrate
./docker/manage.sh createsuperuser
./docker/manage.sh collectstatic

# 4. Access application
open http://localhost:8000
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django Web    │    │   PostgreSQL    │
│   (Node.js)     │────│   Application   │────│   Database      │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Celery        │    │   Redis         │
                       │   Worker/Beat   │────│   Cache/Broker  │
                       │                 │    │   Port: 6379    │
                       └─────────────────┘    └─────────────────┘
```

## 📦 Services

| Service | Description | Port | Health Check |
|---------|-------------|------|--------------|
| **web** | Django application | 8000 | HTTP /admin/login/ |
| **postgres** | PostgreSQL database | 5432 | pg_isready |
| **redis** | Cache & message broker | 6379 | Redis ping |
| **celery** | Background task worker | - | - |
| **celery-beat** | Task scheduler | - | - |
| **frontend** | Development server | 3000 | (dev only) |
| **mailhog** | Email testing | 8025 | (dev only) |
| **adminer** | Database admin | 8080 | (dev only) |

## 🔧 Configuration

### Environment Files

- **`.env.development`** - Safe defaults for local development
- **`.env.example`** - Template for production deployment
- **`.env`** - Your local configuration (auto-created)

### Key Settings

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True/False
ALLOWED_HOSTS=localhost,yourdomain.com

# Database
POSTGRES_DB=strafrecht
POSTGRES_USER=django
POSTGRES_PASSWORD=secure_password

# AWS SES (Email)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
DEFAULT_FROM_EMAIL=webmaster@yourdomain.com
```

## 🛠️ Management Commands

The `./docker/manage.sh` script provides all essential operations:

### Setup & Control
```bash
./docker/manage.sh setup [dev|prod]  # Initial setup
./docker/manage.sh up [dev|prod]     # Start services
./docker/manage.sh down              # Stop services
./docker/manage.sh restart           # Restart all services
./docker/manage.sh build             # Build images
```

### Development
```bash
./docker/manage.sh logs [service]    # View logs
./docker/manage.sh shell [service]   # Access container shell
./docker/manage.sh status            # Show service status
```

### Django Operations
```bash
./docker/manage.sh migrate           # Run database migrations
./docker/manage.sh collectstatic     # Collect static files
./docker/manage.sh createsuperuser   # Create admin user
```

### Maintenance
```bash
./docker/manage.sh backup            # Backup database
./docker/manage.sh restore [file]    # Restore database
./docker/manage.sh clean             # Clean up containers
```

## 🔄 Development Workflow

### 1. Daily Development
```bash
# Start development environment
./docker/manage.sh up

# View logs in real-time
./docker/manage.sh logs web

# Access Django shell
./docker/manage.sh shell web
python manage.py shell
```

### 2. Code Changes
- **Python code**: Auto-reloads in development mode
- **Frontend**: Run `npm run dev` in frontend container
- **Static files**: Run `./docker/manage.sh collectstatic`

### 3. Database Changes
```bash
# Create migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
./docker/manage.sh migrate
```

## 🚀 Production Deployment

### 1. Setup Production Environment
```bash
./docker/manage.sh setup prod
```

### 2. Configure Production Settings
Edit `.env` with production values:
```bash
DEBUG=False
SECRET_KEY=very-secure-random-key
ALLOWED_HOSTS=yourdomain.com
SITE_URL=https://yourdomain.com

# Strong passwords
POSTGRES_PASSWORD=very-secure-password
REDIS_PASSWORD=very-secure-password

# Real AWS credentials
AWS_ACCESS_KEY_ID=production-key
AWS_SECRET_ACCESS_KEY=production-secret
```

### 3. Deploy
```bash
./docker/manage.sh build
./docker/manage.sh up prod
./docker/manage.sh migrate
./docker/manage.sh collectstatic
```

## 🔍 Troubleshooting

### Common Issues

**Services won't start:**
```bash
# Check service status
./docker/manage.sh status

# View error logs
./docker/manage.sh logs
```

**Port conflicts:**
```bash
# Change ports in .env
WEB_PORT=8001
POSTGRES_PORT=5433
```

**Permission errors:**
```bash
# Fix permissions
sudo chown -R $USER:$USER .
chmod +x docker/*.sh
```

**Database connection issues:**
```bash
# Test database connection
docker-compose exec postgres pg_isready
```

### Reset Everything
```bash
# Nuclear option - removes all data
./docker/manage.sh clean
./docker/manage.sh setup dev
./docker/manage.sh up
```

## 📚 Additional Documentation

- **[Complete Docker Deployment Guide](docs/DOCKER_DEPLOYMENT.md)** - Detailed documentation
- **[Main README](README.md)** - Project overview and traditional setup
- **[AWS SES Migration Guide](docs/AWS_SES_MIGRATION_GUIDE.md)** - Email configuration

## 🆘 Need Help?

1. Check logs: `./docker/manage.sh logs`
2. Verify configuration in `.env`
3. Review the troubleshooting section above
4. Check [Docker Deployment Guide](docs/DOCKER_DEPLOYMENT.md) for detailed information

---

**Happy containerizing! 🐳**
