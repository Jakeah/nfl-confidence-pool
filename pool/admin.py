from django.contrib import admin
from .models import Season, Week, Team, Game, ConfidencePick, SurvivorPick, UserSeasonStats, WeeklyResult


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['year', 'is_active', 'created_at']
    list_filter = ['is_active']
    ordering = ['-year']


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = ['season', 'week_number', 'is_active', 'picks_deadline', 'survivor_picks_required']
    list_filter = ['season', 'is_active']
    ordering = ['-season__year', 'week_number']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['abbreviation', 'city', 'name']
    search_fields = ['name', 'abbreviation', 'city']
    ordering = ['city', 'name']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['week', 'away_team', 'home_team', 'game_day', 'game_time', 'is_final', 'score_display']
    list_filter = ['week__season', 'week__week_number', 'game_day', 'is_final']
    search_fields = ['home_team__name', 'away_team__name']
    ordering = ['-week__season__year', 'week__week_number', 'game_time']

    def score_display(self, obj):
        if obj.is_final and obj.home_score is not None and obj.away_score is not None:
            return f"{obj.away_score} - {obj.home_score}"
        return "Not Final"
    score_display.short_description = 'Score (Away-Home)'


@admin.register(ConfidencePick)
class ConfidencePickAdmin(admin.ModelAdmin):
    list_display = ['user', 'game', 'picked_team', 'confidence_points', 'is_correct', 'created_at']
    list_filter = ['game__week__season', 'game__week__week_number', 'picked_team']
    search_fields = ['user__email', 'user__username']
    ordering = ['-created_at']


@admin.register(SurvivorPick)
class SurvivorPickAdmin(admin.ModelAdmin):
    list_display = ['user', 'week', 'picked_team', 'is_correct', 'created_at']
    list_filter = ['week__season', 'week__week_number', 'is_correct']
    search_fields = ['user__email', 'user__username', 'picked_team__name']
    ordering = ['-week__season__year', 'week__week_number']


@admin.register(UserSeasonStats)
class UserSeasonStatsAdmin(admin.ModelAdmin):
    list_display = ['user', 'season', 'playoff_points', 'total_confidence_points', 'survivor_strikes', 'is_eliminated_survivor']
    list_filter = ['season', 'is_eliminated_survivor']
    search_fields = ['user__email', 'user__username']
    ordering = ['-season__year', '-playoff_points', '-total_confidence_points']


@admin.register(WeeklyResult)
class WeeklyResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'week', 'confidence_points', 'weekly_rank', 'playoff_points']
    list_filter = ['week__season', 'week__week_number']
    search_fields = ['user__email', 'user__username']
    ordering = ['-week__season__year', 'week__week_number', '-confidence_points']
