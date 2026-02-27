from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from .models import Season, Week, Game, ConfidencePick, SurvivorPick, Team, UserSeasonStats, WeeklyResult
from .forms import WeekPicksForm, SurvivorPickForm


def home(request):
    context = {}
    if request.user.is_authenticated:
        # Get active season and week
        active_season = Season.objects.filter(is_active=True).first()
        active_week = Week.objects.filter(is_active=True).first()

        context['active_season'] = active_season
        context['active_week'] = active_week

        if active_season:
            # Get user stats for active season
            user_stats, created = UserSeasonStats.objects.get_or_create(
                user=request.user,
                season=active_season
            )
            context['user_stats'] = user_stats

            # Get top 5 leaderboard
            leaderboard = UserSeasonStats.objects.filter(
                season=active_season
            ).select_related('user').order_by('-playoff_points', '-total_confidence_points')[:5]
            context['leaderboard'] = leaderboard

    return render(request, 'pool/home.html', context)


@login_required
def make_picks(request, week_id):
    week = get_object_or_404(Week, id=week_id)
    games = Game.objects.filter(week=week).order_by('game_time')

    # Check if picks deadline has passed
    if timezone.now() > week.picks_deadline:
        messages.error(request, "The deadline for making picks has passed for this week.")
        return redirect('pool:home')

    # Get or create user season stats
    user_stats, created = UserSeasonStats.objects.get_or_create(
        user=request.user,
        season=week.season
    )

    # Get the Bears team
    bears_team = Team.objects.get(abbreviation='CHI')

    # Get existing picks
    existing_confidence_picks = ConfidencePick.objects.filter(
        user=request.user,
        game__week=week
    ).select_related('game', 'picked_team')

    existing_survivor_picks = SurvivorPick.objects.filter(
        user=request.user,
        week=week
    ).select_related('picked_team')

    # Build initial data dict for existing picks
    initial_data = {}
    for pick in existing_confidence_picks:
        initial_data[f'game_{pick.game.id}_team'] = pick.picked_team.id
        initial_data[f'game_{pick.game.id}_confidence'] = pick.confidence_points

    for i, pick in enumerate(existing_survivor_picks):
        initial_data[f'survivor_pick_{i+1}'] = pick.picked_team.id

    if request.method == 'POST':
        confidence_form = WeekPicksForm(request.POST, week=week, user=request.user)
        survivor_form = SurvivorPickForm(request.POST, week=week, user=request.user)

        if confidence_form.is_valid() and (user_stats.is_eliminated_survivor or survivor_form.is_valid()):
            # Delete existing picks for this week
            ConfidencePick.objects.filter(user=request.user, game__week=week).delete()
            SurvivorPick.objects.filter(user=request.user, week=week).delete()

            # Create new confidence picks
            for game in games:
                team_id = int(confidence_form.cleaned_data[f'game_{game.id}_team'])
                confidence = confidence_form.cleaned_data[f'game_{game.id}_confidence']

                ConfidencePick.objects.create(
                    user=request.user,
                    game=game,
                    picked_team_id=team_id,
                    confidence_points=confidence
                )

            # Create new survivor picks (if not eliminated)
            if not user_stats.is_eliminated_survivor:
                num_picks = week.survivor_picks_required()
                for i in range(num_picks):
                    team_id = int(survivor_form.cleaned_data[f'survivor_pick_{i+1}'])
                    SurvivorPick.objects.create(
                        user=request.user,
                        week=week,
                        picked_team_id=team_id
                    )

            messages.success(request, "Your picks have been saved!")
            return redirect('pool:home')
        else:
            # Form has errors - build dict from POST data to retain values
            post_picks_dict = {}
            for game in games:
                team_field = f'game_{game.id}_team'
                confidence_field = f'game_{game.id}_confidence'
                if team_field in request.POST:
                    post_picks_dict[game.id] = {
                        'team_id': int(request.POST[team_field]) if request.POST[team_field] else None,
                        'confidence': int(request.POST[confidence_field]) if request.POST.get(confidence_field) else None
                    }
            existing_picks_dict = post_picks_dict
    else:
        # Load forms with initial data
        confidence_form = WeekPicksForm(initial=initial_data, week=week, user=request.user)
        survivor_form = SurvivorPickForm(initial=initial_data, week=week, user=request.user)

    # Build dictionaries for template access
    existing_picks_dict = {}
    for pick in existing_confidence_picks:
        existing_picks_dict[pick.game.id] = {
            'team_id': pick.picked_team.id,
            'confidence': pick.confidence_points
        }

    context = {
        'week': week,
        'games': games,
        'confidence_form': confidence_form,
        'survivor_form': survivor_form,
        'user_stats': user_stats,
        'bears_team': bears_team,
        'existing_picks': existing_picks_dict,
    }

    return render(request, 'pool/make_picks.html', context)


@login_required
def leaderboard(request, season_id=None):
    if season_id:
        season = get_object_or_404(Season, id=season_id)
    else:
        season = Season.objects.filter(is_active=True).first()

    if not season:
        messages.error(request, "No active season found.")
        return redirect('pool:home')

    standings = UserSeasonStats.objects.filter(
        season=season
    ).select_related('user').order_by('-playoff_points', '-total_confidence_points')

    # Get weekly results for the season
    weekly_results = WeeklyResult.objects.filter(
        week__season=season
    ).select_related('user', 'week').order_by('week__week_number', '-confidence_points')

    context = {
        'season': season,
        'standings': standings,
        'weekly_results': weekly_results,
    }

    return render(request, 'pool/leaderboard.html', context)
