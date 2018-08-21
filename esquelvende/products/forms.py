from django import forms

from .models import ImagesProduct, Product
from .constants import STATUS_CHOICES


class FormProduct(forms.ModelForm):
    title = forms.CharField(max_length=30)
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super(FormProduct, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = None
        self.fields['category'].widget.attrs.update({'onChange': 'categorySelector(event)', 'size': '11', 'class': 'select-category'})
        self.fields['contact_email'].widget=forms.TextInput(attrs={'class': 'form-control'})
        self.fields['price'].widget=forms.TextInput(attrs={'class': 'form-control'})
        self.fields['contact_phone'].widget=forms.TextInput(attrs={'class': 'form-control'})
        self.fields['title'].widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'check', 'data-maxlength': '60'})
        self.fields['description'].widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'})
        self.fields['whatsapp'].widget=forms.TextInput(attrs= {'class': 'form-control', 'title':'Se creara un enlace que permetira al comprador comenzar un chat contigo, sin necesidad de tener tu numero agendado.'})

    class Meta:
        model = Product
        fields = (
            'title',
            'category',
            'subA',
            'subB',
            'subC',
            'brands',
            'status',
            'contact_phone',
            'whatsapp',
            'contact_email',
            'description',
            'price'
        )


class FormImagesProduct(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    def __init__(self, *args, **kwargs):
        super(FormImagesProduct, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['image'].widget.attrs.update({'class': 'form-control-file',
                                                'onchange': 'uploadFile(this.files); displacement()', 'accept': 'image/*'})

    class Meta:
        model = ImagesProduct
        fields = ('image',)


class FormEditProduct(forms.ModelForm):
    title = forms.CharField(max_length=30)

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
