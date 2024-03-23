from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('users/profile/', views.profile, name='profile'),
#   path('add_platform/', views.add_platform, name='add_platform'),
#   path('add_game/', views.add_game, name='add_game'),
  path('accounts/signup/', views.signup, name='signup'),
]