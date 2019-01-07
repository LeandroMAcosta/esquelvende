# -- coding: utf-8 --
import StringIO
from PIL import Image

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Account

class FormEditUser(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormEditUser, self).__init__(*args, **kwargs)
        # self.fields['first_name'].required = True
        # self.fields['last_name'].required = True
        # self.fields['password'].widget  = forms.PasswordInput(attrs = {'class': 'form-control input-cstm', 'placeholder': u'Contraseña'})
        # self.fields['username'].widget  = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['first_name'].widget= forms.TextInput(attrs = {'class': 'form-control input-cstm','placeholder': 'Nombre'})
        self.fields['last_name'].widget = forms.TextInput(attrs = {'class': 'form-control input-cstm','placeholder': 'Apellido'})
        self.fields['email'].widget     = forms.TextInput(attrs = {'class': 'form-control input-cstm','placeholder': 'Email'})

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email')

class FormEditAccount(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormEditAccount, self).__init__(*args, **kwargs)
        self.fields['phone'].widget = forms.TextInput(attrs = {'class': 'form-control input-cstm','placeholder': 'Celular'})

    class Meta:
        model = Account
        fields = ('phone',)

class FormAvatar(forms.ModelForm):

    avatar = forms.ImageField(label="avatar")
    # , widget = forms.HiddenInput()
    class Meta:
        model = Account
        fields = ('avatar',)

    # def clean_avatar(self):
    #     image_field = self.cleaned_data.get('avatar')
    #     image_file = StringIO.StringIO(image_field.read())
    #     image = Image.open(image_file)
    #     w, h = image.size
    #     image = image.resize((w, h), Image.ANTIALIAS)
    #     image_file = StringIO.StringIO()
    #     image.save(image_file, 'JPEG', quality=90)
    #     image_field.file = image_file
    #     return image_field

