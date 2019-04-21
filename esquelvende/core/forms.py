# -- coding: utf-8 --
from django import forms
from django.contrib.auth.forms import (UserChangeForm, UserCreationForm,
                                       AuthenticationForm)
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from account.models import Account


class FormRegister(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': u'Confirmar contraseña'}),
    )

    def __init__(self, *args, **kwargs):
        super(FormRegister, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        help_texts = {
            'username': None,
        }
        fields = ('username', 'first_name', 'last_name', 'email', 'password',
                  'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if (email and User.objects.filter(email=email).
                exclude(username=username).exists()):
            raise forms.ValidationError(u'Email ya esta en uso')
        return email

    def password_matched(self):
        if self.data['password'] != self.data['password2']:
            self.errors['password'] = {u"Contraseñas no coinciden"}
            return False
        else:
            return True

    def is_valid(self):
        valid = super(FormRegister, self).is_valid()
        password_matched = self.password_matched()
        return valid and password_matched

    def save(self, commit=True):
        instance = super(FormRegister, self).save(commit=False)
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        instance.set_password(password)
        instance.username = username

        if commit:
            instance.save()
            Account.objects.create(user=instance)

        return instance, password


class FormLogin(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')
