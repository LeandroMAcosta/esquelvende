# -- coding: utf-8 --
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Favorite


class FavoriteForm(forms.ModelForm):

    class Meta:
        model = Favorite
        fields = []
