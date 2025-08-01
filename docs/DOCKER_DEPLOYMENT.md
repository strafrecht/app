# Docker Deployment Guide for Strafrecht Online

This guide covers containerized deployment of the Strafrecht Online Wagtail Django application using Docker and Docker Compose.

## 🐳 Overview

The containerized setup includes:
- **Django Web Application** (Python 3.10)
- **PostgreSQL Database** (v14)
- **Redis Cache & Session Store** (v7)
- **Celery Worker** for background tasks
- **Celery Beat** for scheduled tasks
- **Frontend Build System** (Node.js 18 + Webpack)

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git (for cloning the repository)

## 🚀 Quick Start

### 1. Initial Setup

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd strafrecht-online

# Switch to containerization branch
git checkout feature/containerization

# Run the setup script
./docker/manage.sh setup dev
```

### 2. Start Development Environment

```bash
# Start all services
./docker/manage.sh up dev

# Or use docker-compose directly
docker-compose up -d
```

### 3. Initialize the Application

```bash
# Run database migrations
./docker/manage.sh migrate

# Create a superuser
./docker/manage.sh createsuperuser

# Collect static files
./docker/manage.sh collectstatic
```

### 4. Access the Application

- **Web Application**: http://localhost:8000
- **Admin Interface**: http://localhost:8000/admin/
- **Database Admin** (Adminer): http://localhost:8080
- **Email Testing** (MailHog): http://localhost:8025

## 🔧 Configuration

### Environment Variables

The application uses environment variables for configuration. Key files:

- `.env.example` - Template for production
- `.env.development` - Development defaults
- `.env` - Your local configuration (created from template)

### Key Configuration Options

```bash
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True/False
ALLOWED_HOSTS=localhost,yourdomain.com

# Database
POSTGRES_DB=strafrecht
POSTGRES_USER=django
POSTGRES_PASSWORD=secure_password

# AWS SES Email
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_SES_REGION=eu-central-1
```

## 🛠️ Development Workflow

### Using the Management Script

The `./docker/manage.sh` script provides convenient commands:

```bash
# View all available commands
./docker/manage.sh help

# Common development tasks
./docker/manage.sh logs web          # View web service logs
./docker/manage.sh shell web         # Access web container shell
./docker/manage.sh restart           # Restart all services
./docker/manage.sh status            # Show service status
```

### Live Code Editing

In development mode, your local code is mounted into containers:
- Changes to Python code trigger Django's auto-reload
- Frontend changes can be built with `npm run dev` in the frontend container
- Database and media files persist in Docker volumes

### Running Management Commands

```bash
# Django management commands
docker-compose exec web python manage.py <command>

# Examples
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py test
docker-compose exec web python manage.py makemigrations
```

## 🏭 Production Deployment

### 1. Production Setup

```bash
# Setup for production
./docker/manage.sh setup prod

# Edit .env with production values
nano .env
```

### 2. Production Configuration

Key production settings in `.env`:

```bash
DEBUG=False
SECRET_KEY=very-secure-random-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SITE_URL=https://yourdomain.com

# Use strong passwords
POSTGRES_PASSWORD=very-secure-db-password
REDIS_PASSWORD=very-secure-redis-password

# Real AWS SES credentials
AWS_ACCESS_KEY_ID=your-production-key
AWS_SECRET_ACCESS_KEY=your-production-secret
```

### 3. Start Production Services

```bash
# Build and start production services
./docker/manage.sh build
./docker/manage.sh up prod
```

### 4. SSL/TLS and Reverse Proxy

For production, use a reverse proxy (nginx/Traefik) for:
- SSL/TLS termination
- Static file serving
- Load balancing

Example nginx configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /path/to/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/media/;
    }
}
```

## 📊 Monitoring and Maintenance

### Health Checks

All services include health checks:
- Web application: HTTP endpoint check
- PostgreSQL: Connection test
- Redis: Ping test

### Logging

```bash
# View logs for all services
./docker/manage.sh logs

# View logs for specific service
./docker/manage.sh logs web
./docker/manage.sh logs celery

# Follow logs in real-time
docker-compose logs -f
```

### Database Backups

```bash
# Create backup
./docker/manage.sh backup

# Restore from backup
./docker/manage.sh restore backups/backup_20231201_120000.sql
```

### Updates and Maintenance

```bash
# Pull latest images
docker-compose pull

# Rebuild after code changes
./docker/manage.sh build

# Clean up old containers/images
./docker/manage.sh clean
```

## 🔍 Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check what's using the port
   lsof -i :8000
   
   # Change ports in .env file
   WEB_PORT=8001
   ```

2. **Permission Issues**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   chmod +x docker/*.sh
   ```

3. **Database Connection Issues**
   ```bash
   # Check database status
   docker-compose exec postgres pg_isready
   
   # View database logs
   docker-compose logs postgres
   ```

4. **Static Files Not Loading**
   ```bash
   # Rebuild frontend
   ./docker/build-frontend.sh
   
   # Collect static files
   ./docker/manage.sh collectstatic
   ```

### Service Dependencies

Services start in this order:
1. PostgreSQL & Redis
2. Django Web Application
3. Celery Worker & Beat

If services fail to start, check:
- Environment variables are set correctly
- No port conflicts exist
- Docker has sufficient resources

### Performance Tuning

For production, consider:
- Increasing worker processes in Dockerfile
- Configuring PostgreSQL connection pooling
- Setting up Redis persistence
- Implementing proper caching strategies

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Wagtail Deployment Guide](https://docs.wagtail.org/en/stable/advanced_topics/deploying.html)
- [AWS SES Documentation](https://docs.aws.amazon.com/ses/)

## 📝 Quick Reference

### Essential Commands

```bash
# Setup and start
./docker/manage.sh setup dev && ./docker/manage.sh up

# Daily development
./docker/manage.sh logs web     # Check logs
./docker/manage.sh shell web    # Access container
./docker/manage.sh restart      # Restart services

# Database operations
./docker/manage.sh migrate      # Run migrations
./docker/manage.sh backup       # Backup database
./docker/manage.sh createsuperuser  # Create admin user

# Maintenance
./docker/manage.sh collectstatic    # Update static files
./docker/manage.sh clean           # Clean up containers
```

### File Structure

```
strafrecht-online/
├── docker/
│   ├── manage.sh              # Main management script
│   ├── setup-env.sh          # Environment setup
│   └── build-frontend.sh     # Frontend build script
├── Dockerfile                # Production container
├── Dockerfile.dev           # Development container
├── docker-compose.yml       # Main services definition
├── docker-compose.override.yml  # Development overrides
├── .env.example             # Environment template
├── .env.development         # Development defaults
└── app/vars_docker.py.tpl   # Django config for containers
```

## 🆘 Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review service logs: `./docker/manage.sh logs`
3. Verify environment configuration
4. Check Docker and system resources
