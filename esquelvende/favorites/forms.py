# -- coding: utf-8 --
from django import forms
from .models import Favorite
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class FavoriteForm(forms.ModelForm):

	#def __init__(self, arg):
	#	super(FavoriteForm, self).__init__()
	#	self.arg = arg
		
	class Meta:
		model = Favorite
		fields = []