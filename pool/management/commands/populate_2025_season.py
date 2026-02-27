from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta, UTC
from pool.models import Season, Week, Game, Team

class Command(BaseCommand):
    help = 'Populate the 2025 NFL season with all weeks and games'

    def handle(self, *args, **options):
        # Create or get 2025 season
        season, created = Season.objects.get_or_create(
            year=2025,
            defaults={'is_active': True}
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created 2025 season'))
        else:
            self.stdout.write(self.style.WARNING(f'2025 season already exists'))

        # Deactivate 2024 season
        Season.objects.filter(year=2024).update(is_active=False)

        self.stdout.write(self.style.SUCCESS('Starting to populate weeks and games...'))

        # Week 1 - September 6-7, 2025
        self.create_week_1(season)
        self.create_week_2(season)
        self.create_week_3(season)
        self.create_week_4(season)
        self.create_week_5(season)
        self.create_week_6(season)
        self.create_week_7(season)
        self.create_week_8(season)
        self.create_week_9(season)
        self.create_week_10(season)
        self.create_week_11(season)
        self.create_week_12(season)
        self.create_week_13(season)
        self.create_week_14(season)
        self.create_week_15(season)
        self.create_week_16(season)
        self.create_week_17(season)
        self.create_week_18(season)

        self.stdout.write(self.style.SUCCESS('\n2025 Season populated successfully!'))

    def create_week_1(self, season):
        """Week 1: September 6-7, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=1,
            defaults={
                'picks_deadline': datetime(2025, 9, 6, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        # Saturday September 6
        games = [
            ('PIT', 'KC', datetime(2025, 9, 6, 16, 30), 'Saturday'),
        ]

        # Sunday September 7
        sunday_games = [
            ('ATL', 'PHI', datetime(2025, 9, 7, 17, 0), 'Sunday'),
            ('IND', 'HOU', datetime(2025, 9, 7, 17, 0), 'Sunday'),
            ('CHI', 'GB', datetime(2025, 9, 7, 17, 0), 'Sunday'),
            ('NE', 'CIN', datetime(2025, 9, 7, 17, 0), 'Sunday'),
            ('MIA', 'JAX', datetime(2025, 9, 7, 17, 0), 'Sunday'),
            ('MIN', 'NYG', datetime(2025, 9, 7, 17, 0), 'Sunday'),
            ('ARI', 'BUF', datetime(2025, 9, 7, 17, 0), 'Sunday'),
            ('TB', 'WAS', datetime(2025, 9, 7, 17, 0), 'Sunday'),
            ('TEN', 'DAL', datetime(2025, 9, 7, 17, 0), 'Sunday'),
            ('CAR', 'NO', datetime(2025, 9, 7, 17, 0), 'Sunday'),
            ('LV', 'LAC', datetime(2025, 9, 7, 20, 5), 'Sunday'),
            ('DEN', 'SEA', datetime(2025, 9, 7, 20, 25), 'Sunday'),
            ('CLE', 'LAR', datetime(2025, 9, 7, 20, 25), 'Sunday'),
        ]

        games.extend(sunday_games)

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)

            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={
                    'game_time': game_time,
                    'game_day': day
                }
            )

        self.stdout.write(f'  Week 1: {len(games)} games created')

    def create_week_2(self, season):
        """Week 2: September 13-14, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=2,
            defaults={
                'picks_deadline': datetime(2025, 9, 13, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('BAL', 'LV', datetime(2025, 9, 14, 17, 0), 'Sunday'),
            ('LAC', 'CAR', datetime(2025, 9, 14, 17, 0), 'Sunday'),
            ('NO', 'TB', datetime(2025, 9, 14, 17, 0), 'Sunday'),
            ('NYG', 'WAS', datetime(2025, 9, 14, 17, 0), 'Sunday'),
            ('SEA', 'NE', datetime(2025, 9, 14, 17, 0), 'Sunday'),
            ('NYJ', 'TEN', datetime(2025, 9, 14, 17, 0), 'Sunday'),
            ('LAR', 'ARI', datetime(2025, 9, 14, 17, 0), 'Sunday'),
            ('SF', 'MIN', datetime(2025, 9, 14, 17, 0), 'Sunday'),
            ('CLE', 'JAX', datetime(2025, 9, 14, 17, 0), 'Sunday'),
            ('CHI', 'HOU', datetime(2025, 9, 14, 17, 0), 'Sunday'),
            ('DAL', 'ATL', datetime(2025, 9, 14, 20, 5), 'Sunday'),
            ('PIT', 'DEN', datetime(2025, 9, 14, 20, 25), 'Sunday'),
            ('DET', 'GB', datetime(2025, 9, 14, 20, 25), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 2: {len(games)} games created')

    def create_week_3(self, season):
        """Week 3: September 20-21, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=3,
            defaults={
                'picks_deadline': datetime(2025, 9, 20, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('PHI', 'NO', datetime(2025, 9, 21, 17, 0), 'Sunday'),
            ('DEN', 'TB', datetime(2025, 9, 21, 17, 0), 'Sunday'),
            ('GB', 'TEN', datetime(2025, 9, 21, 17, 0), 'Sunday'),
            ('HOU', 'MIN', datetime(2025, 9, 21, 17, 0), 'Sunday'),
            ('CHI', 'IND', datetime(2025, 9, 21, 17, 0), 'Sunday'),
            ('MIA', 'CLE', datetime(2025, 9, 21, 17, 0), 'Sunday'),
            ('LAC', 'PIT', datetime(2025, 9, 21, 17, 0), 'Sunday'),
            ('NYG', 'DAL', datetime(2025, 9, 21, 17, 0), 'Sunday'),
            ('CAR', 'LV', datetime(2025, 9, 21, 20, 5), 'Sunday'),
            ('SF', 'LAR', datetime(2025, 9, 21, 20, 25), 'Sunday'),
            ('JAX', 'BUF', datetime(2025, 9, 21, 20, 25), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 3: {len(games)} games created')

    def create_week_4(self, season):
        """Week 4: September 27-28, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=4,
            defaults={
                'picks_deadline': datetime(2025, 9, 27, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('NE', 'SF', datetime(2025, 9, 28, 17, 0), 'Sunday'),
            ('CAR', 'CIN', datetime(2025, 9, 28, 17, 0), 'Sunday'),
            ('CHI', 'LAR', datetime(2025, 9, 28, 17, 0), 'Sunday'),
            ('JAX', 'HOU', datetime(2025, 9, 28, 17, 0), 'Sunday'),
            ('WAS', 'ARI', datetime(2025, 9, 28, 17, 0), 'Sunday'),
            ('DEN', 'NYJ', datetime(2025, 9, 28, 17, 0), 'Sunday'),
            ('MIN', 'GB', datetime(2025, 9, 28, 17, 0), 'Sunday'),
            ('IND', 'PIT', datetime(2025, 9, 28, 17, 0), 'Sunday'),
            ('TB', 'PHI', datetime(2025, 9, 28, 17, 0), 'Sunday'),
            ('CLE', 'LV', datetime(2025, 9, 28, 20, 5), 'Sunday'),
            ('KC', 'LAC', datetime(2025, 9, 28, 20, 25), 'Sunday'),
            ('BUF', 'BAL', datetime(2025, 9, 28, 20, 25), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 4: {len(games)} games created')

    def create_week_5(self, season):
        """Week 5: October 4-5, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=5,
            defaults={
                'picks_deadline': datetime(2025, 10, 4, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('CAR', 'CHI', datetime(2025, 10, 5, 13, 0), 'Sunday'),
            ('MIA', 'NE', datetime(2025, 10, 5, 13, 0), 'Sunday'),
            ('CIN', 'BAL', datetime(2025, 10, 5, 13, 0), 'Sunday'),
            ('IND', 'JAX', datetime(2025, 10, 5, 13, 0), 'Sunday'),
            ('BUF', 'HOU', datetime(2025, 10, 5, 13, 0), 'Sunday'),
            ('ARI', 'SF', datetime(2025, 10, 5, 16, 5), 'Sunday'),
            ('LV', 'DEN', datetime(2025, 10, 5, 16, 25), 'Sunday'),
            ('GB', 'LAR', datetime(2025, 10, 5, 16, 25), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 5: {len(games)} games created')

    def create_week_6(self, season):
        """Week 6: October 11-12, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=6,
            defaults={
                'picks_deadline': datetime(2025, 10, 11, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('TB', 'NO', datetime(2025, 10, 12, 13, 0, tzinfo=UTC), 'Sunday'),
            ('CLE', 'PHI', datetime(2025, 10, 12, 13, 0, tzinfo=UTC), 'Sunday'),
            ('HOU', 'NE', datetime(2025, 10, 12, 13, 0, tzinfo=UTC), 'Sunday'),
            ('ARI', 'GB', datetime(2025, 10, 12, 13, 0, tzinfo=UTC), 'Sunday'),
            ('WAS', 'BAL', datetime(2025, 10, 12, 13, 0, tzinfo=UTC), 'Sunday'),
            ('JAX', 'CHI', datetime(2025, 10, 12, 13, 0, tzinfo=UTC), 'Sunday'),
            ('LAC', 'DEN', datetime(2025, 10, 12, 16, 5, tzinfo=UTC), 'Sunday'),
            ('ATL', 'CAR', datetime(2025, 10, 12, 16, 25, tzinfo=UTC), 'Sunday'),
            ('PIT', 'LV', datetime(2025, 10, 12, 16, 25, tzinfo=UTC), 'Sunday'),
            ('LAR', 'SEA', datetime(2025, 10, 12, 16, 25, tzinfo=UTC), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 6: {len(games)} games created')

    def create_week_7(self, season):
        """Week 7: October 18-19, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=7,
            defaults={
                'picks_deadline': datetime(2025, 10, 18, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('HOU', 'GB', datetime(2025, 10, 19, 13, 0, tzinfo=UTC), 'Sunday'),
            ('NE', 'JAX', datetime(2025, 10, 19, 13, 0, tzinfo=UTC), 'Sunday'),
            ('CIN', 'CLE', datetime(2025, 10, 19, 13, 0, tzinfo=UTC), 'Sunday'),
            ('PHI', 'NYG', datetime(2025, 10, 19, 13, 0, tzinfo=UTC), 'Sunday'),
            ('MIA', 'IND', datetime(2025, 10, 19, 13, 0, tzinfo=UTC), 'Sunday'),
            ('LV', 'LAR', datetime(2025, 10, 19, 13, 0, tzinfo=UTC), 'Sunday'),
            ('TEN', 'BUF', datetime(2025, 10, 19, 13, 0, tzinfo=UTC), 'Sunday'),
            ('DET', 'MIN', datetime(2025, 10, 19, 13, 0, tzinfo=UTC), 'Sunday'),
            ('CHI', 'WAS', datetime(2025, 10, 19, 13, 0, tzinfo=UTC), 'Sunday'),
            ('ATL', 'TB', datetime(2025, 10, 19, 16, 5, tzinfo=UTC), 'Sunday'),
            ('NYJ', 'PIT', datetime(2025, 10, 19, 16, 25, tzinfo=UTC), 'Sunday'),
            ('SF', 'DAL', datetime(2025, 10, 19, 16, 25, tzinfo=UTC), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 7: {len(games)} games created')

    def create_week_8(self, season):
        """Week 8: October 25-26, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=8,
            defaults={
                'picks_deadline': datetime(2025, 10, 25, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('BAL', 'CLE', datetime(2025, 10, 26, 13, 0, tzinfo=UTC), 'Sunday'),
            ('NO', 'LAC', datetime(2025, 10, 26, 13, 0, tzinfo=UTC), 'Sunday'),
            ('ARI', 'MIA', datetime(2025, 10, 26, 13, 0, tzinfo=UTC), 'Sunday'),
            ('IND', 'CHI', datetime(2025, 10, 26, 13, 0, tzinfo=UTC), 'Sunday'),
            ('TEN', 'DET', datetime(2025, 10, 26, 13, 0, tzinfo=UTC), 'Sunday'),
            ('ATL', 'DAL', datetime(2025, 10, 26, 16, 5, tzinfo=UTC), 'Sunday'),
            ('PHI', 'CIN', datetime(2025, 10, 26, 16, 25, tzinfo=UTC), 'Sunday'),
            ('DEN', 'CAR', datetime(2025, 10, 26, 16, 25, tzinfo=UTC), 'Sunday'),
            ('BUF', 'SEA', datetime(2025, 10, 26, 16, 25, tzinfo=UTC), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 8: {len(games)} games created')

    def create_week_9(self, season):
        """Week 9: November 1-2, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=9,
            defaults={
                'picks_deadline': datetime(2025, 11, 1, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('MIA', 'BUF', datetime(2025, 11, 2, 13, 0, tzinfo=UTC), 'Sunday'),
            ('JAX', 'PHI', datetime(2025, 11, 2, 13, 0, tzinfo=UTC), 'Sunday'),
            ('LAC', 'CLE', datetime(2025, 11, 2, 13, 0, tzinfo=UTC), 'Sunday'),
            ('CHI', 'ARI', datetime(2025, 11, 2, 13, 0, tzinfo=UTC), 'Sunday'),
            ('NO', 'CAR', datetime(2025, 11, 2, 13, 0, tzinfo=UTC), 'Sunday'),
            ('NE', 'TEN', datetime(2025, 11, 2, 13, 0, tzinfo=UTC), 'Sunday'),
            ('WAS', 'NYG', datetime(2025, 11, 2, 13, 0, tzinfo=UTC), 'Sunday'),
            ('DEN', 'BAL', datetime(2025, 11, 2, 13, 0, tzinfo=UTC), 'Sunday'),
            ('DAL', 'ATL', datetime(2025, 11, 2, 13, 0, tzinfo=UTC), 'Sunday'),
            ('LV', 'CIN', datetime(2025, 11, 2, 16, 5, tzinfo=UTC), 'Sunday'),
            ('LAR', 'SEA', datetime(2025, 11, 2, 16, 25, tzinfo=UTC), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 9: {len(games)} games created')

    def create_week_10(self, season):
        """Week 10: November 8-9, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=10,
            defaults={
                'picks_deadline': datetime(2025, 11, 8, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('ATL', 'NO', datetime(2025, 11, 9, 13, 0, tzinfo=UTC), 'Sunday'),
            ('NE', 'CHI', datetime(2025, 11, 9, 13, 0, tzinfo=UTC), 'Sunday'),
            ('BUF', 'IND', datetime(2025, 11, 9, 13, 0, tzinfo=UTC), 'Sunday'),
            ('MIN', 'JAX', datetime(2025, 11, 9, 13, 0, tzinfo=UTC), 'Sunday'),
            ('SF', 'TB', datetime(2025, 11, 9, 13, 0, tzinfo=UTC), 'Sunday'),
            ('PIT', 'WAS', datetime(2025, 11, 9, 13, 0, tzinfo=UTC), 'Sunday'),
            ('DEN', 'KC', datetime(2025, 11, 9, 13, 0, tzinfo=UTC), 'Sunday'),
            ('NYJ', 'ARI', datetime(2025, 11, 9, 16, 5, tzinfo=UTC), 'Sunday'),
            ('TEN', 'LAC', datetime(2025, 11, 9, 16, 25, tzinfo=UTC), 'Sunday'),
            ('DET', 'GB', datetime(2025, 11, 9, 16, 25, tzinfo=UTC), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 10: {len(games)} games created')

    def create_week_11(self, season):
        """Week 11: November 15-16, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=11,
            defaults={
                'picks_deadline': datetime(2025, 11, 15, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('JAX', 'DET', datetime(2025, 11, 16, 13, 0, tzinfo=UTC), 'Sunday'),
            ('LV', 'MIA', datetime(2025, 11, 16, 13, 0, tzinfo=UTC), 'Sunday'),
            ('MIN', 'TEN', datetime(2025, 11, 16, 13, 0, tzinfo=UTC), 'Sunday'),
            ('LAR', 'NE', datetime(2025, 11, 16, 13, 0, tzinfo=UTC), 'Sunday'),
            ('CLE', 'NO', datetime(2025, 11, 16, 13, 0, tzinfo=UTC), 'Sunday'),
            ('IND', 'NYJ', datetime(2025, 11, 16, 13, 0, tzinfo=UTC), 'Sunday'),
            ('GB', 'CHI', datetime(2025, 11, 16, 13, 0, tzinfo=UTC), 'Sunday'),
            ('SEA', 'SF', datetime(2025, 11, 16, 16, 5, tzinfo=UTC), 'Sunday'),
            ('KC', 'BUF', datetime(2025, 11, 16, 16, 25, tzinfo=UTC), 'Sunday'),
            ('BAL', 'PIT', datetime(2025, 11, 16, 16, 25, tzinfo=UTC), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 11: {len(games)} games created')

    def create_week_12(self, season):
        """Week 12: November 22-23, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=12,
            defaults={
                'picks_deadline': datetime(2025, 11, 22, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('CHI', 'DET', datetime(2025, 11, 23, 13, 0, tzinfo=UTC), 'Sunday'),
            ('LV', 'DEN', datetime(2025, 11, 23, 13, 0, tzinfo=UTC), 'Sunday'),
            ('MIA', 'NE', datetime(2025, 11, 23, 13, 0, tzinfo=UTC), 'Sunday'),
            ('DAL', 'NYG', datetime(2025, 11, 23, 13, 0, tzinfo=UTC), 'Sunday'),
            ('TB', 'CAR', datetime(2025, 11, 23, 13, 0, tzinfo=UTC), 'Sunday'),
            ('KC', 'CAR', datetime(2025, 11, 23, 13, 0, tzinfo=UTC), 'Sunday'),
            ('HOU', 'TEN', datetime(2025, 11, 23, 13, 0, tzinfo=UTC), 'Sunday'),
            ('ARI', 'SEA', datetime(2025, 11, 23, 16, 5, tzinfo=UTC), 'Sunday'),
            ('LAC', 'BAL', datetime(2025, 11, 23, 16, 25, tzinfo=UTC), 'Sunday'),
            ('PHI', 'LAR', datetime(2025, 11, 23, 16, 25, tzinfo=UTC), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 12: {len(games)} games created')

    def create_week_13(self, season):
        """Week 13: November 29-30, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=13,
            defaults={
                'picks_deadline': datetime(2025, 11, 29, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('SEA', 'CHI', datetime(2025, 11, 30, 13, 0, tzinfo=UTC), 'Sunday'),
            ('LAC', 'ATL', datetime(2025, 11, 30, 13, 0, tzinfo=UTC), 'Sunday'),
            ('IND', 'NE', datetime(2025, 11, 30, 13, 0, tzinfo=UTC), 'Sunday'),
            ('PIT', 'CIN', datetime(2025, 11, 30, 13, 0, tzinfo=UTC), 'Sunday'),
            ('LAR', 'NO', datetime(2025, 11, 30, 13, 0, tzinfo=UTC), 'Sunday'),
            ('TB', 'CAR', datetime(2025, 11, 30, 13, 0, tzinfo=UTC), 'Sunday'),
            ('TEN', 'WAS', datetime(2025, 11, 30, 13, 0, tzinfo=UTC), 'Sunday'),
            ('ARI', 'NYJ', datetime(2025, 11, 30, 16, 5, tzinfo=UTC), 'Sunday'),
            ('PHI', 'BAL', datetime(2025, 11, 30, 16, 25, tzinfo=UTC), 'Sunday'),
            ('GB', 'MIA', datetime(2025, 11, 30, 16, 25, tzinfo=UTC), 'Sunday'),
            ('SF', 'BUF', datetime(2025, 11, 30, 16, 25, tzinfo=UTC), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 13: {len(games)} games created')

    def create_week_14(self, season):
        """Week 14: December 6-7, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=14,
            defaults={
                'picks_deadline': datetime(2025, 12, 6, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('ATL', 'MIN', datetime(2025, 12, 7, 13, 0, tzinfo=UTC), 'Sunday'),
            ('CAR', 'PHI', datetime(2025, 12, 7, 13, 0, tzinfo=UTC), 'Sunday'),
            ('NYJ', 'MIA', datetime(2025, 12, 7, 13, 0, tzinfo=UTC), 'Sunday'),
            ('NO', 'NYG', datetime(2025, 12, 7, 13, 0, tzinfo=UTC), 'Sunday'),
            ('JAX', 'TEN', datetime(2025, 12, 7, 13, 0, tzinfo=UTC), 'Sunday'),
            ('PIT', 'CLE', datetime(2025, 12, 7, 13, 0, tzinfo=UTC), 'Sunday'),
            ('LV', 'TB', datetime(2025, 12, 7, 13, 0, tzinfo=UTC), 'Sunday'),
            ('CHI', 'SF', datetime(2025, 12, 7, 16, 5, tzinfo=UTC), 'Sunday'),
            ('BUF', 'LAR', datetime(2025, 12, 7, 16, 25, tzinfo=UTC), 'Sunday'),
            ('SEA', 'ARI', datetime(2025, 12, 7, 16, 25, tzinfo=UTC), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 14: {len(games)} games created')

    def create_week_15(self, season):
        """Week 15: December 13-14, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=15,
            defaults={
                'picks_deadline': datetime(2025, 12, 13, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('LAR', 'SF', datetime(2025, 12, 14, 13, 0, tzinfo=UTC), 'Sunday'),
            ('NYG', 'BAL', datetime(2025, 12, 14, 13, 0, tzinfo=UTC), 'Sunday'),
            ('CIN', 'TEN', datetime(2025, 12, 14, 13, 0, tzinfo=UTC), 'Sunday'),
            ('MIA', 'HOU', datetime(2025, 12, 14, 13, 0, tzinfo=UTC), 'Sunday'),
            ('WAS', 'NO', datetime(2025, 12, 14, 13, 0, tzinfo=UTC), 'Sunday'),
            ('DAL', 'CAR', datetime(2025, 12, 14, 13, 0, tzinfo=UTC), 'Sunday'),
            ('JAX', 'NYJ', datetime(2025, 12, 14, 13, 0, tzinfo=UTC), 'Sunday'),
            ('NE', 'ARI', datetime(2025, 12, 14, 16, 5, tzinfo=UTC), 'Sunday'),
            ('IND', 'DEN', datetime(2025, 12, 14, 16, 25, tzinfo=UTC), 'Sunday'),
            ('DET', 'BUF', datetime(2025, 12, 14, 16, 25, tzinfo=UTC), 'Sunday'),
            ('CHI', 'MIN', datetime(2025, 12, 14, 16, 25, tzinfo=UTC), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 15: {len(games)} games created')

    def create_week_16(self, season):
        """Week 16: December 20-21, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=16,
            defaults={
                'picks_deadline': datetime(2025, 12, 20, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('CLE', 'CIN', datetime(2025, 12, 21, 13, 0, tzinfo=UTC), 'Sunday'),
            ('TEN', 'IND', datetime(2025, 12, 21, 13, 0, tzinfo=UTC), 'Sunday'),
            ('ARI', 'CAR', datetime(2025, 12, 21, 13, 0, tzinfo=UTC), 'Sunday'),
            ('NYG', 'ATL', datetime(2025, 12, 21, 13, 0, tzinfo=UTC), 'Sunday'),
            ('LAC', 'NE', datetime(2025, 12, 21, 13, 0, tzinfo=UTC), 'Sunday'),
            ('DET', 'CHI', datetime(2025, 12, 21, 13, 0, tzinfo=UTC), 'Sunday'),
            ('PHI', 'WAS', datetime(2025, 12, 21, 13, 0, tzinfo=UTC), 'Sunday'),
            ('BUF', 'NYJ', datetime(2025, 12, 21, 13, 0, tzinfo=UTC), 'Sunday'),
            ('MIN', 'SEA', datetime(2025, 12, 21, 16, 5, tzinfo=UTC), 'Sunday'),
            ('BAL', 'PIT', datetime(2025, 12, 21, 16, 25, tzinfo=UTC), 'Sunday'),
            ('LAR', 'NYJ', datetime(2025, 12, 21, 16, 25, tzinfo=UTC), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 16: {len(games)} games created')

    def create_week_17(self, season):
        """Week 17: December 27-28, 2025"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=17,
            defaults={
                'picks_deadline': datetime(2025, 12, 27, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('GB', 'MIN', datetime(2025, 12, 28, 13, 0, tzinfo=UTC), 'Sunday'),
            ('CAR', 'TB', datetime(2025, 12, 28, 13, 0, tzinfo=UTC), 'Sunday'),
            ('NYJ', 'BUF', datetime(2025, 12, 28, 13, 0, tzinfo=UTC), 'Sunday'),
            ('JAX', 'LV', datetime(2025, 12, 28, 13, 0, tzinfo=UTC), 'Sunday'),
            ('NO', 'MIA', datetime(2025, 12, 28, 13, 0, tzinfo=UTC), 'Sunday'),
            ('CIN', 'DEN', datetime(2025, 12, 28, 13, 0, tzinfo=UTC), 'Sunday'),
            ('TEN', 'JAX', datetime(2025, 12, 28, 13, 0, tzinfo=UTC), 'Sunday'),
            ('CHI', 'SEA', datetime(2025, 12, 28, 16, 5, tzinfo=UTC), 'Sunday'),
            ('LAC', 'NE', datetime(2025, 12, 28, 16, 25, tzinfo=UTC), 'Sunday'),
            ('KC', 'PIT', datetime(2025, 12, 28, 16, 25, tzinfo=UTC), 'Sunday'),
            ('ATL', 'WAS', datetime(2025, 12, 28, 16, 25, tzinfo=UTC), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 17: {len(games)} games created')

    def create_week_18(self, season):
        """Week 18: January 3-4, 2026"""
        week, _ = Week.objects.get_or_create(
            season=season,
            week_number=18,
            defaults={
                'picks_deadline': datetime(2026, 1, 3, 12, 0, tzinfo=UTC),
                'is_active': False
            }
        )

        games = [
            ('MIA', 'NYJ', datetime(2026, 1, 4, 13, 0, tzinfo=UTC), 'Sunday'),
            ('CHI', 'GB', datetime(2026, 1, 4, 13, 0, tzinfo=UTC), 'Sunday'),
            ('CAR', 'ATL', datetime(2026, 1, 4, 13, 0, tzinfo=UTC), 'Sunday'),
            ('NO', 'TB', datetime(2026, 1, 4, 13, 0, tzinfo=UTC), 'Sunday'),
            ('CLE', 'BAL', datetime(2026, 1, 4, 13, 0, tzinfo=UTC), 'Sunday'),
            ('IND', 'JAX', datetime(2026, 1, 4, 13, 0, tzinfo=UTC), 'Sunday'),
            ('LAR', 'SEA', datetime(2026, 1, 4, 16, 25, tzinfo=UTC), 'Sunday'),
            ('KC', 'DEN', datetime(2026, 1, 4, 16, 25, tzinfo=UTC), 'Sunday'),
            ('DAL', 'PHI', datetime(2026, 1, 4, 16, 25, tzinfo=UTC), 'Sunday'),
            ('SF', 'ARI', datetime(2026, 1, 4, 16, 25, tzinfo=UTC), 'Sunday'),
        ]

        for away_abbr, home_abbr, game_time, day in games:
            away_team = Team.objects.get(abbreviation=away_abbr)
            home_team = Team.objects.get(abbreviation=home_abbr)
            Game.objects.get_or_create(
                week=week,
                home_team=home_team,
                away_team=away_team,
                defaults={'game_time': game_time, 'game_day': day}
            )

        self.stdout.write(f'  Week 18: {len(games)} games created')
