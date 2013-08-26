# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from twitter import Api
from twitter_app.forms import UserDetailsForm, ProfileForm
from twitter_app.models import Country, Profile
from twitter_mapping.settings import CONSUMER_KEY, ACCESS_TOKEN_SECRET, ACCESS_TOKEN_KEY, CONSUMER_SECRET
from django.contrib.auth.models import User

from django.contrib.auth import logout

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


def index(request):
    api = Api(consumer_key=CONSUMER_KEY,
              consumer_secret=CONSUMER_SECRET,
              access_token_key=ACCESS_TOKEN_KEY,
              access_token_secret=ACCESS_TOKEN_SECRET)
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if profile.twitter_name is not '':
        user_id = profile.twitter_name
    else:
        user_id = request.user.username
    if request.method == "GET":
        if 'user' in request.GET:
            user_id = request.GET['user']
    twitter = api.GetUserTimeline(screen_name=user_id, count=10)  # premature optimization atm would be to cache request to twitter
    twitter_user = api.GetUser(screen_name=user_id)
    country_list = Country.objects.values('name', 'longitude', 'latitude')
    for tweet in twitter:  # this is horribly slow atm, could speed this up if I thought about it harder.
        for country in country_list:
            if country['name'] in tweet.text:  # stupid simple search method, doesn't rank countries by relevance
                tweet.country = {'name': country['name'],
                                 'latitude': country['latitude'],
                                 'longitude': country['longitude']}
                break

    return render(request, 'index.html', {'twitter': twitter, 'twitter_user': twitter_user})

@login_required
def user_details(request, username):
    if request.user.username != username:
        username = request.user.username
        return redirect(reverse('user_details', kwargs={'username': username}))
    else:
        if request.method == "POST":
            user_form = UserDetailsForm(request.POST, instance=request.user)
            profile, _ = Profile.objects.get_or_create(user=request.user)
            twitter_form = ProfileForm(request.POST, instance=profile)
            if user_form.is_valid() and twitter_form.is_valid():
                user_form.save()
                twitter_form.save()
                return redirect(reverse('index'))
        else:
            user_form = UserDetailsForm(instance=request.user)
            profile, _ = Profile.objects.get_or_create(user=request.user)
            twitter_form = ProfileForm(instance=profile)
        return render(request, 'user_details.html', {'user_form': user_form, 'twitter_form': twitter_form})
