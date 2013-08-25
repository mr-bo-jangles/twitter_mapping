# Create your views here.
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from twitter import Api
from twitter_app.models import Country
from twitter_mapping.settings import CONSUMER_KEY, ACCESS_TOKEN_SECRET, ACCESS_TOKEN_KEY, CONSUMER_SECRET

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


def index(request):
    api = Api(consumer_key=CONSUMER_KEY,
              consumer_secret=CONSUMER_SECRET,
              access_token_key=ACCESS_TOKEN_KEY,
              access_token_secret=ACCESS_TOKEN_SECRET)
    user_id = "Giggaflop"
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