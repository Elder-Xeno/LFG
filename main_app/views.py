from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Profile

def home(request):
    return render(request, 'home.html')

@login_required
def profile(request, username=None):
    if username is None:
        username = request.user.username
    user_profile = get_object_or_404(Profile, user__username=username)
    return render(request, 'users/profile.html', {'user_profile': user_profile})


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
        pass
    else:
        return render(request, 'add_game.html')

@login_required
def add_platform(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'add_platform.html')

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