from django.urls import path
from .views import get_usernames

urlpatterns = [
    path('usernames/', get_usernames, name='get_usernames'),
]