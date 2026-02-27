from django.core.management.base import BaseCommand
from pool.models import Team


class Command(BaseCommand):
    help = 'Populate the database with all 32 NFL teams'

    def handle(self, *args, **options):
        teams_data = [
            # AFC East
            {'city': 'Buffalo', 'name': 'Bills', 'abbreviation': 'BUF'},
            {'city': 'Miami', 'name': 'Dolphins', 'abbreviation': 'MIA'},
            {'city': 'New England', 'name': 'Patriots', 'abbreviation': 'NE'},
            {'city': 'New York', 'name': 'Jets', 'abbreviation': 'NYJ'},

            # AFC North
            {'city': 'Baltimore', 'name': 'Ravens', 'abbreviation': 'BAL'},
            {'city': 'Cincinnati', 'name': 'Bengals', 'abbreviation': 'CIN'},
            {'city': 'Cleveland', 'name': 'Browns', 'abbreviation': 'CLE'},
            {'city': 'Pittsburgh', 'name': 'Steelers', 'abbreviation': 'PIT'},

            # AFC South
            {'city': 'Houston', 'name': 'Texans', 'abbreviation': 'HOU'},
            {'city': 'Indianapolis', 'name': 'Colts', 'abbreviation': 'IND'},
            {'city': 'Jacksonville', 'name': 'Jaguars', 'abbreviation': 'JAX'},
            {'city': 'Tennessee', 'name': 'Titans', 'abbreviation': 'TEN'},

            # AFC West
            {'city': 'Denver', 'name': 'Broncos', 'abbreviation': 'DEN'},
            {'city': 'Kansas City', 'name': 'Chiefs', 'abbreviation': 'KC'},
            {'city': 'Las Vegas', 'name': 'Raiders', 'abbreviation': 'LV'},
            {'city': 'Los Angeles', 'name': 'Chargers', 'abbreviation': 'LAC'},

            # NFC East
            {'city': 'Dallas', 'name': 'Cowboys', 'abbreviation': 'DAL'},
            {'city': 'New York', 'name': 'Giants', 'abbreviation': 'NYG'},
            {'city': 'Philadelphia', 'name': 'Eagles', 'abbreviation': 'PHI'},
            {'city': 'Washington', 'name': 'Commanders', 'abbreviation': 'WAS'},

            # NFC North
            {'city': 'Chicago', 'name': 'Bears', 'abbreviation': 'CHI'},
            {'city': 'Detroit', 'name': 'Lions', 'abbreviation': 'DET'},
            {'city': 'Green Bay', 'name': 'Packers', 'abbreviation': 'GB'},
            {'city': 'Minnesota', 'name': 'Vikings', 'abbreviation': 'MIN'},

            # NFC South
            {'city': 'Atlanta', 'name': 'Falcons', 'abbreviation': 'ATL'},
            {'city': 'Carolina', 'name': 'Panthers', 'abbreviation': 'CAR'},
            {'city': 'New Orleans', 'name': 'Saints', 'abbreviation': 'NO'},
            {'city': 'Tampa Bay', 'name': 'Buccaneers', 'abbreviation': 'TB'},

            # NFC West
            {'city': 'Arizona', 'name': 'Cardinals', 'abbreviation': 'ARI'},
            {'city': 'Los Angeles', 'name': 'Rams', 'abbreviation': 'LAR'},
            {'city': 'San Francisco', 'name': '49ers', 'abbreviation': 'SF'},
            {'city': 'Seattle', 'name': 'Seahawks', 'abbreviation': 'SEA'},
        ]

        created_count = 0
        updated_count = 0

        for team_data in teams_data:
            team, created = Team.objects.get_or_create(
                abbreviation=team_data['abbreviation'],
                defaults={
                    'city': team_data['city'],
                    'name': team_data['name']
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {team}')
                )
            else:
                # Update existing team in case data changed
                team.city = team_data['city']
                team.name = team_data['name']
                team.save()
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created: {created_count}, Updated: {updated_count}, Total: {Team.objects.count()}'
            )
        )
