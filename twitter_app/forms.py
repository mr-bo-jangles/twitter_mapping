from django.contrib.auth.models import User
from django.forms import ModelForm, forms
from twitter_app.models import Profile


class UserDetailsForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['twitter_name']