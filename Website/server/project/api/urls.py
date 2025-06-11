from django.urls import path
from .views import get_usernames, create_usernames, usernames_detail, create_multiple_usernames
urlpatterns = [
    path('usernames/', get_usernames, name='get_usernames'),
    path('usernames/create/', create_usernames, name='create_usernames'),
    path('usernames/create-multiple/', create_multiple_usernames, name='create_multiple_usernames'),
    path('usernames/<int:pk>/', usernames_detail, name='usernames_detail'),

]