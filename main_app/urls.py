from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
  path('', LoginView.as_view(), name='login'),
  path('accounts/login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('profile/edit/', views.edit_profile, name='edit_profile'),
  path('profile/delete_picture/', views.delete_profile_picture, name='delete_profile_image'),  
  path('profile/', views.profile, name='profile'),
  path('profile/<str:username>/', views.profile, name='profile'),
  path('add_platform/', views.add_platform, name='add_platform'),
  path('add_game/', views.add_game, name='add_game'),
  path('accounts/signup/', views.signup, name='signup'),
  path('search/', views.user_search, name='user_search'),
  path('platforms/<int:platform_id>/dissociate/', views.dissociate_platform, name='dissociate_platform'),
  path('games/<int:game_id>/dissociate/', views.dissociate_game, name='dissociate_game'),
]