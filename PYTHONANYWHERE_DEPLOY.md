# PythonAnywhere Deployment Guide

## Step 1: Create PythonAnywhere Account
1. Go to https://www.pythonanywhere.com/
2. Sign up for a free "Beginner" account
3. Confirm your email

## Step 2: Upload Your Code

### Option A: Using Git (Recommended)
1. First, push your code to GitHub (if not done yet)
2. Open a **Bash console** in PythonAnywhere
3. Clone your repository:
```bash
git clone https://github.com/YOUR_USERNAME/nfl-confidence-pool.git
cd nfl-confidence-pool
```

### Option B: Upload Files Directly
1. Go to the "Files" tab in PythonAnywhere
2. Upload your project files
3. Navigate to `/home/YOUR_USERNAME/nfl-confidence-pool/`

## Step 3: Set Up Virtual Environment
In the Bash console:
```bash
cd ~/nfl-confidence-pool
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 4: Configure Database
```bash
# Still in the virtual environment
python manage.py migrate
python manage.py createsuperuser  # Create your admin account
python manage.py populate_teams
python manage.py populate_2025_season
python manage.py collectstatic --noinput
```

## Step 5: Set Up Web App
1. Go to the **Web** tab in PythonAnywhere
2. Click "Add a new web app"
3. Choose "Manual configuration" (NOT Django)
4. Select **Python 3.11**

## Step 6: Configure WSGI File
1. In the Web tab, click on the WSGI configuration file link
2. Delete all the existing content
3. Paste this configuration:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/YOUR_USERNAME/nfl-confidence-pool'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SECRET_KEY'] = 'your-secret-key-here-generate-a-new-one'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'YOUR_USERNAME.pythonanywhere.com'

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'nfl_pool.settings'

# Activate your virtual environment
activate_this = '/home/YOUR_USERNAME/nfl-confidence-pool/venv/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**IMPORTANT**: Replace `YOUR_USERNAME` with your actual PythonAnywhere username in all 3 places!

**Generate a new secret key**: In a Bash console, run:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy the output and use it for `DJANGO_SECRET_KEY` above.

## Step 7: Configure Virtual Environment Path
1. Still in the **Web** tab
2. Find the "Virtualenv" section
3. Enter: `/home/YOUR_USERNAME/nfl-confidence-pool/venv`
4. Click the checkmark to save

## Step 8: Configure Static Files
In the **Web** tab, find the "Static files" section:

1. Add this mapping:
   - URL: `/static/`
   - Directory: `/home/YOUR_USERNAME/nfl-confidence-pool/staticfiles`

## Step 9: Reload Your Web App
1. Scroll to the top of the **Web** tab
2. Click the big green **"Reload"** button
3. Wait 30 seconds

## Step 10: Test Your Site
Visit: `https://YOUR_USERNAME.pythonanywhere.com`

Your NFL Confidence Pool should now be live! 🏈

## Troubleshooting

### Site doesn't load or shows errors
1. Check the **Error log** and **Server log** in the Web tab
2. Most common issues:
   - Wrong username in paths
   - Virtual environment not activated
   - Missing migrations
   - Incorrect ALLOWED_HOSTS

### Database is empty
Run these commands in Bash console:
```bash
cd ~/nfl-confidence-pool
source venv/bin/activate
python manage.py populate_teams
python manage.py populate_2025_season
```

### Static files (CSS) not loading
```bash
cd ~/nfl-confidence-pool
source venv/bin/activate
python manage.py collectstatic --noinput
```
Then reload the web app.

## Updating Your Site Later

When you make changes:
```bash
cd ~/nfl-confidence-pool
git pull origin main  # If using git
source venv/bin/activate
python manage.py migrate  # If database changes
python manage.py collectstatic --noinput  # If static file changes
```

Then reload the web app from the Web tab.

## Free Tier Limitations
- 1 web app only
- YOUR_USERNAME.pythonanywhere.com domain
- 512 MB disk space
- No SSH access
- Manual deployments

Upgrade to paid plan ($5/month) for custom domains and more features.
