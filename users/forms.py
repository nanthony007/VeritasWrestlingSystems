from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from vws_main.models import FS_Wrestler


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['teamname', 'image']


class ProfileRosterUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['roster57', 'roster61', 'roster65', 'roster70', 'roster74', 'roster79',
                  'roster86', 'roster92', 'roster97', 'roster125']
