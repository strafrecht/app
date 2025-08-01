#!/bin/bash

# Docker management script for Strafrecht Online
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to show usage
show_usage() {
    echo "🐳 Strafrecht Online Docker Management Script"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  setup [dev|prod]     - Initial setup (default: dev)"
    echo "  build                - Build all Docker images"
    echo "  up [dev|prod]        - Start services (default: dev)"
    echo "  down                 - Stop services"
    echo "  restart              - Restart services"
    echo "  logs [service]       - View logs (all services or specific)"
    echo "  shell [service]      - Access service shell (default: web)"
    echo "  migrate              - Run database migrations"
    echo "  collectstatic        - Collect static files"
    echo "  createsuperuser      - Create Django superuser"
    echo "  backup               - Backup database"
    echo "  restore [file]       - Restore database from backup"
    echo "  clean                - Clean up containers and volumes"
    echo "  status               - Show service status"
    echo ""
    echo "Examples:"
    echo "  $0 setup dev         - Setup for development"
    echo "  $0 up prod           - Start production services"
    echo "  $0 logs web          - View web service logs"
    echo "  $0 shell celery      - Access celery container shell"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to setup environment
setup_env() {
    local env_type=${1:-dev}
    log_info "Setting up environment for: $env_type"
    
    cd "$PROJECT_DIR"
    bash docker/setup-env.sh "$env_type"
    
    log_success "Environment setup complete"
}

# Function to build images
build_images() {
    log_info "Building Docker images..."
    cd "$PROJECT_DIR"
    
    # Build frontend first
    bash docker/build-frontend.sh
    
    # Build main application
    docker-compose build
    
    log_success "Docker images built successfully"
}

# Function to start services
start_services() {
    local env_type=${1:-dev}
    cd "$PROJECT_DIR"
    
    if [ "$env_type" = "prod" ]; then
        log_info "Starting production services..."
        docker-compose -f docker-compose.yml up -d
    else
        log_info "Starting development services..."
        docker-compose up -d
    fi
    
    log_success "Services started"
}

# Function to stop services
stop_services() {
    log_info "Stopping services..."
    cd "$PROJECT_DIR"
    docker-compose down
    log_success "Services stopped"
}

# Function to restart services
restart_services() {
    log_info "Restarting services..."
    stop_services
    start_services
    log_success "Services restarted"
}

# Function to view logs
view_logs() {
    local service=$1
    cd "$PROJECT_DIR"
    
    if [ -n "$service" ]; then
        log_info "Viewing logs for service: $service"
        docker-compose logs -f "$service"
    else
        log_info "Viewing logs for all services"
        docker-compose logs -f
    fi
}

# Function to access shell
access_shell() {
    local service=${1:-web}
    cd "$PROJECT_DIR"
    
    log_info "Accessing shell for service: $service"
    docker-compose exec "$service" bash
}

# Function to run migrations
run_migrations() {
    log_info "Running database migrations..."
    cd "$PROJECT_DIR"
    docker-compose exec web python manage.py migrate
    log_success "Migrations completed"
}

# Function to collect static files
collect_static() {
    log_info "Collecting static files..."
    cd "$PROJECT_DIR"
    docker-compose exec web python manage.py collectstatic --noinput
    log_success "Static files collected"
}

# Function to create superuser
create_superuser() {
    log_info "Creating Django superuser..."
    cd "$PROJECT_DIR"
    docker-compose exec web python manage.py createsuperuser
    log_success "Superuser created"
}

# Function to backup database
backup_database() {
    log_info "Creating database backup..."
    cd "$PROJECT_DIR"
    
    local backup_file="backups/backup_$(date +%Y%m%d_%H%M%S).sql"
    docker-compose exec postgres pg_dump -U "${POSTGRES_USER:-django}" "${POSTGRES_DB:-strafrecht}" > "$backup_file"
    
    log_success "Database backup created: $backup_file"
}

# Function to restore database
restore_database() {
    local backup_file=$1
    
    if [ -z "$backup_file" ]; then
        log_error "Please specify backup file to restore"
        exit 1
    fi
    
    if [ ! -f "$backup_file" ]; then
        log_error "Backup file not found: $backup_file"
        exit 1
    fi
    
    log_warning "This will overwrite the current database. Are you sure? (y/N)"
    read -r confirm
    
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        log_info "Restoring database from: $backup_file"
        cd "$PROJECT_DIR"
        docker-compose exec -T postgres psql -U "${POSTGRES_USER:-django}" -d "${POSTGRES_DB:-strafrecht}" < "$backup_file"
        log_success "Database restored"
    else
        log_info "Database restore cancelled"
    fi
}

# Function to clean up
clean_up() {
    log_warning "This will remove all containers and volumes. Are you sure? (y/N)"
    read -r confirm
    
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        log_info "Cleaning up containers and volumes..."
        cd "$PROJECT_DIR"
        docker-compose down -v --remove-orphans
        docker system prune -f
        log_success "Cleanup completed"
    else
        log_info "Cleanup cancelled"
    fi
}

# Function to show status
show_status() {
    log_info "Service status:"
    cd "$PROJECT_DIR"
    docker-compose ps
}

# Main script logic
check_docker

case "${1:-help}" in
    setup)
        setup_env "$2"
        ;;
    build)
        build_images
        ;;
    up|start)
        start_services "$2"
        ;;
    down|stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        view_logs "$2"
        ;;
    shell|bash)
        access_shell "$2"
        ;;
    migrate)
        run_migrations
        ;;
    collectstatic)
        collect_static
        ;;
    createsuperuser)
        create_superuser
        ;;
    backup)
        backup_database
        ;;
    restore)
        restore_database "$2"
        ;;
    clean)
        clean_up
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        log_error "Unknown command: $1"
        echo ""
        show_usage
        exit 1
        ;;
esac
