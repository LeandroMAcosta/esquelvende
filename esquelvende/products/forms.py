from django import forms
from .models import Product, ImagesProduct


class FormProduct(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('title', 'category', 'subcategory', 'filter', 'description', 'price')

class FormImagesProduct(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = ImagesProduct
        fields = ('image',)