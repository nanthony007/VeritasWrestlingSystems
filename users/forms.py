from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from vws_main.models import FS_Wrestler
from django_select2.forms import ModelSelect2MultipleWidget


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


class MyWidget(ModelSelect2MultipleWidget):
    queryset = FS_Wrestler.objects.order_by('name')
    search_fields = [
        'name__icontains',
    ]
    max_results = 10


class RosterUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('roster',)
        widgets = {
            'roster': MyWidget,
        }


class LoginForm(forms.Form):
    username = forms.CharField(label=('Username'))
    password = forms.CharField(
        label=('Password'), widget=forms.PasswordInput(render_value=False))
