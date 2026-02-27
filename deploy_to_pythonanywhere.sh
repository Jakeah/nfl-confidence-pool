#!/bin/bash
# PythonAnywhere Deployment Script
# Run this in a PythonAnywhere Bash console

set -e  # Exit on error

echo "🏈 NFL Confidence Pool - PythonAnywhere Deployment"
echo "=================================================="
echo ""

# Clone repository
echo "📦 Cloning repository..."
cd ~
if [ -d "nfl-confidence-pool" ]; then
    echo "Directory exists, pulling latest changes..."
    cd nfl-confidence-pool
    git pull origin main
else
    git clone https://github.com/Jakeah/nfl-confidence-pool.git
    cd nfl-confidence-pool
fi

# Create virtual environment
echo ""
echo "🐍 Setting up virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
echo ""
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup database (CLEAN SLATE - no season data)
echo ""
echo "🗄️  Setting up database..."
python manage.py migrate

echo ""
echo "👥 Creating superuser..."
echo "You'll be prompted to create an admin account:"
python manage.py createsuperuser

echo ""
echo "🏈 Populating NFL teams..."
python manage.py populate_teams

# Collect static files
echo ""
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Setup complete!"
echo ""
echo "=================================================="
echo "NEXT STEPS:"
echo "=================================================="
echo ""
echo "1. Go to the Web tab in PythonAnywhere"
echo "2. Click 'Add a new web app'"
echo "3. Choose 'Manual configuration' and Python 3.11"
echo "4. Configure WSGI file (see below)"
echo "5. Set virtualenv to: $HOME/nfl-confidence-pool/venv"
echo "6. Add static files mapping:"
echo "   URL: /static/"
echo "   Directory: $HOME/nfl-confidence-pool/staticfiles"
echo "7. Click Reload"
echo ""
echo "=================================================="
echo "WSGI FILE CONFIGURATION:"
echo "=================================================="
echo ""
echo "Generate a secret key first:"
echo "python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
echo ""
echo "Then paste this in your WSGI file (replace YOUR_USERNAME and SECRET_KEY):"
echo ""
cat << 'WSGIEOF'
import os
import sys

# Add your project directory to the sys.path
username = os.environ.get('USER', 'YOUR_USERNAME')
path = f'/home/{username}/nfl-confidence-pool'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SECRET_KEY'] = 'PASTE_YOUR_GENERATED_SECRET_KEY_HERE'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_ALLOWED_HOSTS'] = f'{username}.pythonanywhere.com'

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'nfl_pool.settings'

# Activate virtual environment
activate_this = f'/home/{username}/nfl-confidence-pool/venv/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
WSGIEOF

echo ""
echo "=================================================="
echo "🎉 Your site will be live at: https://YOUR_USERNAME.pythonanywhere.com"
echo "=================================================="
