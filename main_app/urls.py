from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
  path('', LoginView.as_view(), name='home'),
  path('users/profile/', views.profile, name='profile'),
  path('add_platform/', views.add_platform, name='add_platform'),
  path('add_game/', views.add_game, name='add_game'),
  path('accounts/signup/', views.signup, name='signup'),
]