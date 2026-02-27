# NFL Confidence Pool

A Django-based web application for running an NFL confidence pool with unique rules including mandatory Chicago Bears picks and an integrated survivor pool.

## Features

- **User Authentication**: Email/password signup and login
- **Confidence Pool**: Pick winners for Saturday/Sunday NFL games with confidence points
- **Mandatory Bears Rule**: Users must pick the Chicago Bears to win every week
- **Survivor Pool**:
  - Odd weeks: pick 1 team
  - Even weeks: pick 2 teams
  - 3 strikes = elimination
  - Cannot reuse teams within a season
- **Multi-Season Support**: Track performance across multiple NFL seasons
- **Real-time Leaderboard**: View standings and track your performance

## Setup

### Prerequisites

- Python 3.13+
- pip

### Installation

1. **Activate Virtual Environment**
   ```bash
   source venv/bin/activate
   ```

2. **Install Dependencies** (already done)
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations** (already done)
   ```bash
   python manage.py migrate
   ```

4. **Populate NFL Teams** (already done)
   ```bash
   python manage.py populate_teams
   ```

5. **Create Admin User**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Admin Setup

As an administrator, you need to set up the season and weeks:

1. **Login to Admin Panel**: http://127.0.0.1:8000/admin/

2. **Create a Season**:
   - Go to "Seasons" → "Add Season"
   - Set the year (e.g., 2026)
   - Mark as "Active"

3. **Create Weeks**:
   - Go to "Weeks" → "Add Week"
   - Select the season
   - Set week number (1-18)
   - Set picks deadline (date/time when picks close)
   - Mark one week as "Active" for current week

4. **Add Games**:
   - Go to "Games" → "Add Game"
   - Select the week
   - Select home and away teams
   - Set game day (Saturday or Sunday only - no Thursday games!)
   - Set game time
   - Save

5. **When Games Complete**:
   - Edit the game in admin
   - Enter home_score and away_score
   - Check "is_final"
   - Save

6. **Score the Week**:
   ```bash
   python manage.py score_games --week-id <week_id>
   ```
   Or score all weeks with final games:
   ```bash
   python manage.py score_games
   ```

## Pool Rules

1. **Chicago Bears Rule**: Every user MUST pick the Chicago Bears to win their game every week
2. **Saturday/Sunday Only**: Only games on Saturday and Sunday count (no Thursday Night Football)
3. **Confidence Points**: Assign unique confidence values from 1 to N (where N = number of weekend games)
   - Higher points = more confident
   - Each game gets a unique value
4. **Survivor Pool**:
   - Odd weeks: pick 1 team to win
   - Even weeks: pick 2 teams to win
   - Cannot reuse teams within the same season
   - 3 incorrect picks = elimination from survivor pool
   - Confidence and survivor pools are scored separately

## Management Commands

- `python manage.py populate_teams` - Populate all 32 NFL teams
- `python manage.py score_games` - Score all weeks with final games
- `python manage.py score_games --week-id <id>` - Score a specific week

## Project Structure

```
nfl_pool/
├── nfl_pool/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── pool/              # Main app
│   ├── models.py      # Database models
│   ├── views.py       # View logic
│   ├── forms.py       # Forms with validation
│   ├── admin.py       # Admin interface
│   ├── templates/     # HTML templates
│   └── management/    # Custom commands
├── requirements.txt   # Python dependencies
└── db.sqlite3        # Database
```

## Models

- **Season**: NFL season (year, active status)
- **Week**: Week within a season (week number, deadline, active status)
- **Team**: NFL team (name, abbreviation, city)
- **Game**: Individual game (teams, date, score, final status)
- **ConfidencePick**: User's pick with confidence points
- **SurvivorPick**: User's survivor pool pick
- **UserSeasonStats**: User statistics (points, strikes, elimination status)

## Contributing

This is a custom pool application. Modify as needed for your pool's specific rules.
