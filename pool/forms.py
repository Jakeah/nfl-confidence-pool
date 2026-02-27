from django import forms
from django.core.exceptions import ValidationError
from .models import ConfidencePick, SurvivorPick, Game, Team, Week


class WeekPicksForm(forms.Form):
    """Form for making confidence picks for a week"""

    def __init__(self, *args, week=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.week = week
        self.user = user

        if not week:
            return

        # Get all Saturday/Sunday games for this week
        games = Game.objects.filter(week=week).order_by('game_time')
        self.games = games
        self.num_games = games.count()

        # Get the Chicago Bears team
        try:
            self.bears = Team.objects.get(abbreviation='CHI')
        except Team.DoesNotExist:
            self.bears = None

        # Create fields for each game
        for game in games:
            # Team selection field
            choices = [
                (game.home_team.id, f"{game.home_team.abbreviation} (Home)"),
                (game.away_team.id, f"{game.away_team.abbreviation} (Away)")
            ]
            self.fields[f'game_{game.id}_team'] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,
                label=f"{game.away_team.abbreviation} @ {game.home_team.abbreviation}"
            )

            # Confidence points field
            self.fields[f'game_{game.id}_confidence'] = forms.IntegerField(
                min_value=1,
                max_value=self.num_games,
                widget=forms.NumberInput(attrs={'class': 'confidence-input'}),
                label='Confidence'
            )

        # Load existing picks if any
        if user:
            existing_picks = ConfidencePick.objects.filter(
                user=user,
                game__week=week
            ).select_related('game', 'picked_team')

            for pick in existing_picks:
                self.fields[f'game_{pick.game.id}_team'].initial = pick.picked_team.id
                self.fields[f'game_{pick.game.id}_confidence'].initial = pick.confidence_points

    def clean(self):
        cleaned_data = super().clean()

        if not self.week or not self.games:
            return cleaned_data

        # Check that Chicago Bears are picked
        bears_picked = False
        confidence_values = []

        for game in self.games:
            team_field = f'game_{game.id}_team'
            confidence_field = f'game_{game.id}_confidence'

            if team_field in cleaned_data and confidence_field in cleaned_data:
                team_id = int(cleaned_data[team_field])
                confidence = cleaned_data[confidence_field]

                # Check if Bears are in this game and if they're picked
                if self.bears and (game.home_team.id == self.bears.id or game.away_team.id == self.bears.id):
                    if team_id == self.bears.id:
                        bears_picked = True

                confidence_values.append(confidence)

        # Validate Bears pick
        if self.bears and not bears_picked:
            raise ValidationError("You must pick the Chicago Bears to win their game!")

        # Validate unique confidence values
        if len(confidence_values) != len(set(confidence_values)):
            raise ValidationError("Each game must have a unique confidence value!")

        # Validate all confidence values from 1 to num_games are used
        expected_values = set(range(1, self.num_games + 1))
        if set(confidence_values) != expected_values:
            raise ValidationError(f"You must use all confidence values from 1 to {self.num_games}!")

        return cleaned_data


class SurvivorPickForm(forms.Form):
    """Form for making survivor picks"""

    def __init__(self, *args, week=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.week = week
        self.user = user

        if not week or not user:
            return

        # Get teams that user has already used for survivor this season
        season = week.season
        used_teams = SurvivorPick.objects.filter(
            user=user,
            week__season=season
        ).values_list('picked_team_id', flat=True)

        # Get all teams except those already used
        available_teams = Team.objects.exclude(id__in=used_teams).order_by('city', 'name')

        team_choices = [(team.id, str(team)) for team in available_teams]

        # Determine number of picks required
        num_picks = week.survivor_picks_required()

        # Create pick fields
        for i in range(num_picks):
            self.fields[f'survivor_pick_{i+1}'] = forms.ChoiceField(
                choices=[('', '-- Select Team --')] + team_choices,
                label=f'Survivor Pick {i+1}',
                required=True
            )

        # Load existing picks
        existing_picks = SurvivorPick.objects.filter(
            user=user,
            week=week
        ).order_by('id')

        for i, pick in enumerate(existing_picks):
            if i < num_picks:
                self.fields[f'survivor_pick_{i+1}'].initial = pick.picked_team.id

    def clean(self):
        cleaned_data = super().clean()

        if not self.week:
            return cleaned_data

        # Get all picked teams
        picked_teams = []
        num_picks = self.week.survivor_picks_required()

        for i in range(num_picks):
            field_name = f'survivor_pick_{i+1}'
            if field_name in cleaned_data and cleaned_data[field_name]:
                picked_teams.append(int(cleaned_data[field_name]))

        # Ensure no duplicate picks in the same week
        if len(picked_teams) != len(set(picked_teams)):
            raise ValidationError("You cannot pick the same team multiple times in one week!")

        return cleaned_data
