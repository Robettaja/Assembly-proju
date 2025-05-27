from django.urls import path
from .views import get_usernames, create_usernames, usernames_detail

urlpatterns = [
    path('usernames/', get_usernames, name='get_usernames'),
    path('usernames/create/', create_usernames, name='create_usernames'),
    path('usernames/<int:pk>/', usernames_detail, name='usernames_detail'),
]