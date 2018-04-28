# -- coding: utf-8 --
from django import forms
from .models import User, UserProfile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

import StringIO
from PIL import Image



class FormRegister(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super(FormRegister, self).__init__(*args, **kwargs)
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		self.fields['password'].widget = forms.PasswordInput()

	class Meta:
		model = User
		help_texts = {
			'username': None,
		}

		fields = ('username', 'password', 'email', 'last_name', 'first_name')

	def clean_email(self):
		email = self.cleaned_data.get('email')
		username = self.cleaned_data.get('username')
		if email and User.objects.filter(email=email).exclude(username=username).exists():
			raise forms.ValidationError(u'Email ya esta en uso')
		return email


class FormEditUser(forms.ModelForm):

	class Meta:
		model = User
		fields = ('last_name', 'first_name', 'email')   
		
class FormAvatar(forms.ModelForm):

	avatar = forms.ImageField(label="avatar")
	
	class Meta:
		model = UserProfile
		fields = ('avatar',)

	
	def clean_avatar(self):
		image_field = self.cleaned_data.get('avatar')
		image_file = StringIO.StringIO(image_field.read())
		image = Image.open(image_file)
		w, h = image.size
		image = image.resize((w/2, h/2), Image.ANTIALIAS)
		image_file = StringIO.StringIO()
		image.save(image_file, 'JPEG', quality=90)
		image_field.file = image_file
		return image_field

