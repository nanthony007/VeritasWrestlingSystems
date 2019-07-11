from django import forms
from vws_main.models import FS_Wrestler


class Wrestler1ModelForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = FS_Wrestler
        fields = ['name', ]


class Wrestler2ModelForm(forms.ModelForm):
    class Meta:
        model = FS_Wrestler
        fields = ['name']
