from django.core.management.base import BaseCommand
from django.db.models import Sum, Q
from pool.models import Week, Game, ConfidencePick, SurvivorPick, UserSeasonStats, WeeklyResult


class Command(BaseCommand):
    help = 'Score completed games and update user statistics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--week-id',
            type=int,
            help='Score a specific week by ID',
        )

    def handle(self, *args, **options):
        week_id = options.get('week_id')

        if week_id:
            weeks = Week.objects.filter(id=week_id)
        else:
            # Score all weeks with final games that haven't been fully scored
            weeks = Week.objects.filter(games__is_final=True).distinct()

        if not weeks.exists():
            self.stdout.write(self.style.WARNING('No weeks found to score.'))
            return

        for week in weeks:
            self.stdout.write(f'\nScoring {week}...')
            self.score_week(week)

        self.stdout.write(self.style.SUCCESS('\nScoring complete!'))

    def score_week(self, week):
        """Score all picks for a given week"""

        # Get all final games for this week
        final_games = week.games.filter(is_final=True)

        if not final_games.exists():
            self.stdout.write(self.style.WARNING(f'  No final games for {week}'))
            return

        # Score confidence picks
        confidence_picks = ConfidencePick.objects.filter(
            game__in=final_games
        ).select_related('user', 'game', 'picked_team')

        points_by_user = {}

        for pick in confidence_picks:
            if pick.user not in points_by_user:
                points_by_user[pick.user] = 0

            if pick.is_correct():
                points_by_user[pick.user] += pick.confidence_points
                self.stdout.write(
                    f'  ✓ {pick.user.email}: +{pick.confidence_points} pts for {pick.picked_team.abbreviation}'
                )
            else:
                self.stdout.write(
                    f'  ✗ {pick.user.email}: 0 pts (picked {pick.picked_team.abbreviation})'
                )

        # Create or update weekly results
        for user, points in points_by_user.items():
            weekly_result, created = WeeklyResult.objects.get_or_create(
                user=user,
                week=week,
                defaults={'confidence_points': points}
            )
            if not created:
                weekly_result.confidence_points = points
                weekly_result.save()

        # Calculate weekly rankings and playoff points
        self.calculate_weekly_rankings(week)

        # Update user season stats for confidence points
        for user, points in points_by_user.items():
            stats, created = UserSeasonStats.objects.get_or_create(
                user=user,
                season=week.season
            )

            # Add points for this week
            stats.total_confidence_points += points
            stats.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'  Updated {user.email}: +{points} pts (Total: {stats.total_confidence_points})'
                )
            )

        # Score survivor picks
        self.score_survivor_picks(week, final_games)

    def calculate_weekly_rankings(self, week):
        """Calculate weekly rankings and award playoff points"""
        # Playoff points based on weekly rank
        PLAYOFF_POINTS = {
            1: 20, 2: 15, 3: 14, 4: 13, 5: 12, 6: 11, 7: 10, 8: 9,
            9: 8, 10: 7, 11: 6, 12: 5, 13: 4, 14: 3, 15: 2, 16: 1
        }

        # Get all weekly results for this week, ordered by points (desc)
        weekly_results = WeeklyResult.objects.filter(week=week).order_by('-confidence_points', 'user__email')

        self.stdout.write(f'\n  📊 Weekly Rankings:')

        rank = 1
        for result in weekly_results:
            result.weekly_rank = rank
            result.playoff_points = PLAYOFF_POINTS.get(rank, 0)
            result.save()

            # Update season playoff points
            stats = UserSeasonStats.objects.get(user=result.user, season=week.season)
            stats.playoff_points += result.playoff_points
            stats.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'    #{rank} {result.user.email}: {result.confidence_points} pts → +{result.playoff_points} playoff pts'
                )
            )

            rank += 1

    def score_survivor_picks(self, week, final_games):
        """Score survivor picks and track strikes"""

        survivor_picks = SurvivorPick.objects.filter(
            week=week
        ).select_related('user', 'picked_team')

        for pick in survivor_picks:
            # Check if pick has already been scored
            if pick.is_correct is not None:
                continue

            # Find the game where the picked team played
            team_game = final_games.filter(
                Q(home_team=pick.picked_team) | Q(away_team=pick.picked_team)
            ).first()

            if not team_game:
                self.stdout.write(
                    self.style.WARNING(
                        f'  No final game found for survivor pick: {pick.user.email} - {pick.picked_team.abbreviation}'
                    )
                )
                continue

            winner = team_game.winner()
            pick.is_correct = (winner == pick.picked_team)
            pick.save()

            # Update user stats
            stats, created = UserSeasonStats.objects.get_or_create(
                user=pick.user,
                season=week.season
            )

            if not pick.is_correct:
                stats.add_survivor_strike()
                self.stdout.write(
                    self.style.ERROR(
                        f'  ⚠ SURVIVOR STRIKE: {pick.user.email} - {pick.picked_team.abbreviation} lost '
                        f'(Strikes: {stats.survivor_strikes}/3)'
                    )
                )
                if stats.is_eliminated_survivor:
                    self.stdout.write(
                        self.style.ERROR(
                            f'  💀 {pick.user.email} ELIMINATED from survivor pool!'
                        )
                    )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✓ Survivor: {pick.user.email} - {pick.picked_team.abbreviation} won'
                    )
                )
