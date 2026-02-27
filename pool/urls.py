from django.urls import path
from . import views

app_name = 'pool'

urlpatterns = [
    path('', views.home, name='home'),
    path('picks/<int:week_id>/', views.make_picks, name='make_picks'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('leaderboard/<int:season_id>/', views.leaderboard, name='leaderboard_season'),
]
