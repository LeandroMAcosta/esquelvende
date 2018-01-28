from django import forms
from .models import Product, ImagesProduct


class FormProduct(forms.ModelForm):
    title = forms.CharField(
        max_length = 30
    )

    class Meta:
        model = Product
        fields = ('title', 'category', 'subcategory', 'filter', 'contact_phone', 'contact_email', 'description', 'price')


class FormImagesProduct(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = ImagesProduct
        fields = ('image',)
