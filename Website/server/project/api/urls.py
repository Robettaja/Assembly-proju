from django.urls import path
from .views import get_usernames, create_usernames

urlpatterns = [
    path('usernames/', get_usernames, name='get_usernames'),
    path('usernames/create/', create_usernames, name='create_usernames'),
]