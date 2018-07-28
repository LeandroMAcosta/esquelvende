# -- coding: utf-8 --
import StringIO

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from PIL import Image

from .models import User, UserProfile


class FormRegister(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder': u'Confirmar contraseña'}),)

    def __init__(self, *args, **kwargs):
        super(FormRegister, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password'].widget  = forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder': u'Contraseña'})
        self.fields['username'].widget  = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['first_name'].widget= forms.TextInput(attrs = {'class': 'form-control','placeholder': 'Nombre'})
        self.fields['last_name'].widget = forms.TextInput(attrs = {'class': 'form-control','placeholder': 'Apellido'})
        self.fields['email'].widget     = forms.TextInput(attrs = {'class': 'form-control','placeholder': 'Email'})
        
    class Meta:
        model = User
        help_texts = {
            'username': None,
        }
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if (email and
                User.objects.filter(email=email).exclude(username=username)
                            .exists()):
            raise forms.ValidationError(u'Email ya esta en uso')
        return email

    def password_matched(self):
        if self.data['password'] != self.data['password2']:
            self.errors['password'] = {u"Contraseñas no coinciden"}
            return False
        else:
            return True

    def is_valid(self):
        valid = super(FormRegister,self).is_valid()
        password_matched = self.password_matched()
        if valid and password_matched:
            return True
        else:
            return False


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


class FormLogin(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget=forms.TextInput(attrs = {'class': 'form-control', 
                                                                'placeholder': 'Nombre de usuario'})

        self.fields['password'].widget=forms.PasswordInput(attrs = {'class': 'form-control', 
                                                                    'placeholder': u'Contraseña'})

