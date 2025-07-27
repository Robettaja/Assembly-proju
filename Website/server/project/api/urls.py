from django.urls import path
from .views import get_usernames, create_usernames, usernames_detail, create_multiple_usernames, bulk_create_laptimes, save_race_session
from . import views

urlpatterns = [
    path('usernames/', get_usernames, name='get_usernames'),
    path('usernames/create/', create_usernames, name='create_usernames'),
    path('usernames/create-multiple/', create_multiple_usernames, name='create_multiple_usernames'),
    path('usernames/<int:pk>/', usernames_detail, name='usernames_detail'),
    path('start/', views.start_race_views),
    path('lap/', views.lap_completed, name='lap_completed'),
    path('save-laps/', views.save_laps, name='save_laps'),
    path('laptimes/bulk_create/', bulk_create_laptimes, name='bulk_create_laptimes'),
    path('race-sessions/save/', save_race_session, name='save_race_session'),
    path('user-laps/<str:username>/', views.get_user_laptimes, name='user-laps')
]