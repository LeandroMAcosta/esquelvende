from django import forms
from .models import User


class FormRegister(forms.ModelForm):

    class Meta:
        model = User
        help_texts = {
            'username': None,
        }
        fields = ('username', 'password', 'email', 'last_name', 'first_name')
