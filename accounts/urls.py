# accounts/urls.py
from django.urls import path
from .views import RegisterView, ObtainAuthTokenView, LogoutView, ProfileView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', ObtainAuthTokenView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]