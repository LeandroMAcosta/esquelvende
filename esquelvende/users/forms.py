# -- coding: utf-8 --
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


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

class FormEditUser(forms.ModelForm):

	#def __init__(self, *args, **kwargs):
	#	super(FormEditUser, self).__init__(*args, **kwargs)
	#	user = self.instance
	#	print user
	#	self.fields['first_name'].initial=user.first_name
		
	#last_name = forms.CharField(initial='apellido',label="Apellido")
	#first_name = forms.CharField(initial='nombre',label="Nombre")
	#email = forms.CharField(initial='mail',label="Email")

	class Meta:
		model = User
		fields = ('last_name', 'first_name', 'email')   
		