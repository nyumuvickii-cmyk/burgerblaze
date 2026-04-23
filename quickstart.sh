#!/bin/bash
# BurgerBlaze Quick Start Script

echo "🍔 BurgerBlaze - Quick Setup"
echo "=============================="

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "✓ Virtual environment created"
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Setup environment variables
echo "⚙️  Setting up environment..."
cp .env.example .env

# Database setup
echo "🗄️  Setting up database..."
python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
python manage.py createsuperuser

# Populate menu
echo "🍽️  Populating menu data..."
python manage.py populate_menu

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the server, run:"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "📋 Admin panel: http://localhost:8000/admin"
echo "🏠 Homepage: http://localhost:8000"
echo "📱 Menu: http://localhost:8000/menu/"
echo ""
