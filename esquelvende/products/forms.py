from django import forms
from .models import Product


class FormProduct(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('title', 'category', 'subcategory', 'filter', 'description', 'price')
