from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
  path('', LoginView.as_view(), name='login'),
  path('accounts/login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('profile/', views.profile, name='profile'),
  path('profile/<str:username>/', views.profile, name='profile'),
  path('add_platform/', views.add_platform, name='add_platform'),
  path('add_game/', views.add_game, name='add_game'),
  path('accounts/signup/', views.signup, name='signup'),
  path('search/', views.user_search, name='user_search'),
]