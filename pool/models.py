from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Season(models.Model):
    year = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.year} Season"


class Week(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='weeks')
    week_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(18)])
    is_active = models.BooleanField(default=False)
    picks_deadline = models.DateTimeField()

    class Meta:
        ordering = ['season', 'week_number']
        unique_together = ['season', 'week_number']

    def __str__(self):
        return f"{self.season.year} - Week {self.week_number}"

    def survivor_picks_required(self):
        """Returns number of survivor picks required for this week"""
        return 2 if self.week_number % 2 == 0 else 1


class Team(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=100)

    class Meta:
        ordering = ['city', 'name']

    def __str__(self):
        return f"{self.city} {self.name}"


class Game(models.Model):
    SATURDAY = 'SAT'
    SUNDAY = 'SUN'

    DAY_CHOICES = [
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    ]

    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='games')
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')
    game_time = models.DateTimeField()
    game_day = models.CharField(max_length=3, choices=DAY_CHOICES)

    # Result fields
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    is_final = models.BooleanField(default=False)

    class Meta:
        ordering = ['game_time']

    def __str__(self):
        return f"{self.away_team.abbreviation} @ {self.home_team.abbreviation} - {self.week}"

    def winner(self):
        """Returns the winning team or None if game not final"""
        if not self.is_final or self.home_score is None or self.away_score is None:
            return None
        if self.home_score > self.away_score:
            return self.home_team
        elif self.away_score > self.home_score:
            return self.away_team
        return None  # Tie (rare but possible)


class ConfidencePick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confidence_picks')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='confidence_picks')
    picked_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    confidence_points = models.IntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [
            ['user', 'game'],  # One pick per game per user
        ]

    def __str__(self):
        return f"{self.user.email} - {self.game} - {self.picked_team.abbreviation} ({self.confidence_points})"

    def is_correct(self):
        """Check if this pick was correct"""
        if not self.game.is_final:
            return None
        winner = self.game.winner()
        return winner == self.picked_team if winner else False


class SurvivorPick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='survivor_picks')
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='survivor_picks')
    picked_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_correct = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['week', 'user']

    def __str__(self):
        return f"{self.user.email} - {self.week} - Survivor: {self.picked_team.abbreviation}"


class UserSeasonStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='season_stats')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='user_stats')
    survivor_strikes = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])
    is_eliminated_survivor = models.BooleanField(default=False)
    total_confidence_points = models.IntegerField(default=0)
    playoff_points = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'season']
        ordering = ['-playoff_points', '-total_confidence_points']

    def __str__(self):
        return f"{self.user.email} - {self.season.year} - Playoff: {self.playoff_points} pts"

    def add_survivor_strike(self):
        """Add a strike and check if user should be eliminated"""
        self.survivor_strikes += 1
        if self.survivor_strikes >= 3:
            self.is_eliminated_survivor = True
        self.save()


class WeeklyResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_results')
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='weekly_results')
    confidence_points = models.IntegerField(default=0)
    weekly_rank = models.IntegerField(null=True, blank=True)
    playoff_points = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'week']
        ordering = ['week', '-confidence_points']

    def __str__(self):
        return f"{self.user.email} - {self.week} - Rank: {self.weekly_rank} - {self.playoff_points} playoff pts"
