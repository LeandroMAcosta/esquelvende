from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class FormRegister(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super(FormRegister, self).__init__(*args, **kwargs)
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True

	class Meta:
		model = User
		help_texts = {
		    'username': None,
		}
		fields = ('username', 'password', 'email', 'last_name', 'first_name')

class FormEditUser(forms.ModelForm):

	class Meta:
		model = User
		fields = ('last_name', 'first_name', 'email')   
		#fields = '__all__'