#!/bin/bash

# Setup script for Strafrecht Online Docker environment
set -e

echo "🐳 Setting up Strafrecht Online Docker environment..."

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p log
mkdir -p media
mkdir -p staticfiles
mkdir -p backups
mkdir -p docker/postgres/init

# Set up environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    if [ "$1" = "development" ] || [ "$1" = "dev" ]; then
        cp .env.development .env
        echo "✅ Development environment file created."
    else
        cp .env.example .env
        echo "⚠️  Production environment template created. Please edit .env with your actual values!"
    fi
else
    echo "ℹ️  .env file already exists, skipping creation."
fi

# Set up vars.py for Docker
echo "🔧 Setting up Django configuration for Docker..."
if [ ! -f app/vars.py ]; then
    cp app/vars_docker.py.tpl app/vars.py
    echo "✅ Docker-specific vars.py created."
else
    echo "ℹ️  app/vars.py already exists. You may want to backup and replace it with vars_docker.py.tpl for Docker deployment."
fi

# Create initial database setup script
cat > docker/postgres/init/01-create-test-db.sql << EOF
-- Create test database for Django tests
CREATE DATABASE \${POSTGRES_DB}_test;
GRANT ALL PRIVILEGES ON DATABASE \${POSTGRES_DB}_test TO \${POSTGRES_USER};
EOF

echo "✅ Database initialization script created."

# Set proper permissions
echo "🔒 Setting proper permissions..."
chmod +x docker/setup-env.sh
chmod 755 log media staticfiles backups

echo ""
echo "🎉 Docker environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run: docker-compose up -d"
echo "3. Run migrations: docker-compose exec web python manage.py migrate"
echo "4. Create superuser: docker-compose exec web python manage.py createsuperuser"
echo "5. Collect static files: docker-compose exec web python manage.py collectstatic"
echo ""
echo "For development:"
echo "- Use: docker-compose -f docker-compose.yml -f docker-compose.override.yml up"
echo "- Or simply: docker-compose up (override is loaded automatically)"
echo ""
echo "Useful commands:"
echo "- View logs: docker-compose logs -f"
echo "- Access shell: docker-compose exec web bash"
echo "- Run management commands: docker-compose exec web python manage.py <command>"
