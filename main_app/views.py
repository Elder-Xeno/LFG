import os
import uuid
import boto3
from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfilePictureForm, EditProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Game, Platform
from django.db.models import Count
from django.http import JsonResponse
from requests import post
from django.http import HttpResponse
from io import BytesIO
# from .utils import search_games_api


PLATFORMS = (
    ('PC', 'PC'),
    ('PS4', 'PlayStation 4'),
    ('PS5', 'PlayStation 5'),
    ('XBOX', 'Xbox One'),
    ('XBOX_SERIES_X', 'Xbox Series X'),
    ('XBOX_SERIES_S', 'Xbox Series S'),
    ('SWITCH_LITE', 'Nintendo Switch Lite'),
    ('SWITCH', 'Nintendo Switch'),
)


def upload_to_aws_s3(file, filename):
    import boto3
    from botocore.exceptions import NoCredentialsError

    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        s3.upload_fileobj(file, AWS_STORAGE_BUCKET_NAME, filename)
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False


@login_required
def upload_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            uploaded_file = request.FILES.get('profile_image', None)
            if uploaded_file:
                try:
                    s3 = boto3.client('s3')
                    bucket = os.environ['S3_BUCKET']
                    key = uuid.uuid4().hex[:6] + uploaded_file.name[uploaded_file.name.rfind('.'):]
                    s3.upload_fileobj(uploaded_file, bucket, key)
                    url = f"{os.environ['S3_BASE_URL']}/{bucket}/{key}"
                    
                    request.user.profile.profile_image = url
                    request.user.profile.save()
                    return redirect('profile')
                except Exception as e:
                    return HttpResponse('An error occurred uploading file to S3: ' + str(e))  # Return error response for debugging
    else:
        form = ProfilePictureForm(instance=request.user.profile)
    return render(request, 'upload_profile_picture.html', {'form': form})



@login_required
def profile(request, username=None):
    if username is None:
        username = request.user.username
    user_profile = get_object_or_404(Profile, user__username=username)
    games_owned = user_profile.games.all()
    return render(request, 'users/profile.html', {'user_profile': user_profile, 'games_owned': games_owned})


@login_required
def dissociate_platform(request, platform_id):
    platform = get_object_or_404(Platform, id=platform_id)
    profile = Profile.objects.get(user=request.user)
    if platform in profile.platforms.all():
        profile.platforms.remove(platform)
    return redirect('profile')

@login_required
def dissociate_game(request, game_id):
    game = Game.objects.get(pk=game_id)
    profile = Profile.objects.get(user=request.user)
    if game in profile.games.all():
        profile.games.remove(game)
        profile.games_owned = profile.games.count()
        profile.save()
    return redirect('profile')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            
            login(request, user)
            return redirect('profile')
        else:
            error_message = 'Invalid sign up - try again'
    else:
        form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def search_games_api(search):
    access_token = "wgc7mftl4uywt7g5xay6tjim4agucq"
    headers = {
        'Client-ID': os.environ.get("CLIENT_ID"), 
        'Authorization': f'Bearer {access_token}'
    }
    response = post('https://api.igdb.com/v4/games', headers=headers, data=f'fields id, name, url; search: "{search}"; where version_parent = null;')
    return response.json()


@login_required
def add_game(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        url = request.POST.get('url')
        platforms = request.POST.getlist('platforms')
        game_data_list = search_games_api(name)
        if game_data_list:
            game_data = game_data_list[0]
            game = Game.objects.create(name=name, url=url)


            for platform_id in platforms:
                platform = Platform.objects.get(pk=platform_id)
                game.platforms.add(platform)
            profile = Profile.objects.get(user=request.user)
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
        platform_codes = request.POST.getlist('name')
        for platform_code in platform_codes:
            platform_name = dict(PLATFORMS)[platform_code]
            platform, created = Platform.objects.get_or_create(name=platform_name)
            profile = Profile.objects.get(user=request.user)
            if platform not in profile.platforms.all():
                profile.platforms.add(platform)
        profile.save()
        return redirect('profile')
    return render(request, 'main_app/add_platform.html', {'platforms': PLATFORMS})


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


from django.core.files.storage import default_storage

def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    edit_mode = False
    
    if request.method == 'POST':
        edit_mode = True
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
                
            if 'profile_image' in request.FILES:
                uploaded_file = request.FILES['profile_image']
                file_name = f"profile_images/{uploaded_file.name}"
                file_path = default_storage.save(file_name, uploaded_file)
                profile.profile_image = default_storage.url(file_path)
                profile.save()

            return redirect('profile')  
    else:
        form = EditProfileForm(instance=profile)

    has_profile_image = bool(profile.profile_image)
    
    edit_profile_url = reverse('edit_profile')

    return render(request, 'main_app/edit_profile.html', {'form': form, 'edit_mode': edit_mode, 'edit_profile_url': edit_profile_url, 'has_profile_image': has_profile_image, 'games_owned': profile.games.all(), 'platforms_owned': profile.platforms.all()})



@login_required
def delete_profile_picture(request):
    profile = Profile.objects.get(user=request.user)
    if profile.profile_image:
        profile.profile_image.delete()
    return redirect('edit_profile')

# def get_twitch_access_token():
#     client_id = os.environ.get("CLIENT_ID") 
#     client_secret = os.environ.get("CLIENT_SECRET") 
#     response = post(f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials')
#     return response