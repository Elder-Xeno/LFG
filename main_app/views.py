from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Game, Platform
from django.db.models import Count
from django.http import JsonResponse
from requests import post
import os


def home(request):
    return render(request, 'home.html')

@login_required
def profile(request, username=None):
    if username is None:
        username = request.user.username
    user_profile = get_object_or_404(Profile, user__username=username)
    games_owned = user_profile.games.all()
    return render(request, 'users/profile.html', {'user_profile': user_profile, 'games_owned': games_owned})


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create a profile for the newly created user
            Profile.objects.create(user=user)
            
            login(request, user)
            return redirect('profile')
        else:
            error_message = 'Invalid sign up - try again'
    else:
        form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def add_game(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        platforms = request.POST.getlist('platforms')
        game = Game.objects.create(name=name)
        for platform_id in platforms:
            platform = Platform.objects.get(pk=platform_id)
            game.platforms.add(platform)
        
        profile = Profile.objects.get(user=request.user)
        for platform_id in platforms:
            platform = Platform.objects.get(pk=platform_id)
            if not profile.platforms.filter(pk=platform_id).exists():
                profile.platforms.add(platform)
        
        profile.games.add(game)
        profile.games_owned = profile.games.count()
        profile.save()
        
        return redirect('profile')
    else:
        games = []
        search = request.GET.get("search")
        if search:
            games = search_games_api(search)

        platforms = Platform.objects.all()
        return render(request, 'main_app/add_game.html', {'platforms': platforms, "games": games})



@login_required
def add_platform(request):
    if request.method == 'POST':
        platform_name = request.POST.get('name')
        platform, created = Platform.objects.get_or_create(name=platform_name)
        profile = Profile.objects.get(user=request.user)
        if platform not in profile.platforms.all():
            profile.platforms.add(platform)
            profile.save()
        
        return redirect('profile')
    else:
        return render(request, 'main_app/add_platform.html')

@login_required
def user_search(request):
    query = request.GET.get('query')
    users = User.objects.filter(username__icontains=query)
    return render(request, 'users/search_results.html', {'results': users})

class CustomLoginView(BaseLoginView):
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(reverse('profile', kwargs={'username': user.username}))




def search_games_api(search):
    access_token = "wgc7mftl4uywt7g5xay6tjim4agucq"
    headers = {
        'Client-ID': os.environ.get("CLIENT_ID"), 
        'Authorization': f'Bearer {access_token}'
    }

    response = post('https://api.igdb.com/v4/games', headers=headers, data=f'fields id, name; search: "{search}"; datetime;')

    return response.json()


# def get_twitch_access_token():
#     client_id = os.environ.get("CLIENT_ID") 
#     client_secret = os.environ.get("CLIENT_SECRET") 

#     response = post(f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials')

#     return response
