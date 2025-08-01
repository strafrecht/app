#!/bin/bash

# Frontend build script for Docker deployment
set -e

echo "🎨 Building frontend assets for Docker deployment..."

# Change to frontend directory
cd frontend

# Check if package.json exists
if [ ! -f package.json ]; then
    echo "❌ package.json not found in frontend directory"
    exit 1
fi

# Check if build already exists
if [ -d build ] && [ "$(ls -A build)" ]; then
    echo "ℹ️  Frontend build directory already exists with content"
    echo "📋 Existing build contents:"
    ls -la build/ | head -10
    echo "✅ Using existing frontend build"
else
    # Install dependencies
    echo "📦 Installing frontend dependencies..."
    if ! npm ci --only=production --legacy-peer-deps; then
        echo "⚠️  npm ci failed, trying with existing node_modules..."
        if [ ! -d node_modules ]; then
            echo "❌ No node_modules found and npm ci failed"
            exit 1
        fi
    fi

    # Build for production
    echo "🔨 Building frontend assets..."
    if ! NODE_ENV=production npm run build; then
        echo "❌ Frontend build failed"
        exit 1
    fi

    # Verify build output
    if [ ! -d build ]; then
        echo "❌ Frontend build failed - build directory not found"
        exit 1
    fi
fi

echo "✅ Frontend build completed successfully"
echo "📁 Build output available in frontend/build/"

# List build contents
echo "📋 Build contents:"
ls -la build/

cd ..
echo "🎉 Frontend build process complete!"
