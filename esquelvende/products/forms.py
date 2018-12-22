from django import forms

from django.forms import ModelChoiceField
from .models import ImagesProduct, Product
from .constants import STATUS_CHOICES

from django.core.exceptions import ValidationError
from categories.models import Category, SubA, SubB, Brand


class FormProduct(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_CHOICES,
                               widget=forms.RadioSelect())
    category = ModelChoiceField(Category.objects.all(), required=False, empty_label=None)

    class Meta:
        model = Product
        fields = (
            'title',
            'category',
            'subA',
            'subB',
            'brands',
            'status',
            'contact_phone',
            'whatsapp',
            'contact_email',
            'description',
            'price'
        )


class FormImagesProduct(forms.ModelForm):

    class Meta:
        model = ImagesProduct
        fields = ('image',)


class FormEditProduct(forms.ModelForm):

    class Meta:
        model = Product
        fields = (
            'title',
            'status',
            'contact_phone',
            'whatsapp',
            'contact_email',
            'description',
            'price'
        )
