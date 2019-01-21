from django import forms

from django.forms import ModelChoiceField
from .models import ImagesProduct, Product, Favorite

from django.core.exceptions import ValidationError
from category.models import Category, SubA, SubB, Brand


class FormProduct(forms.ModelForm):
    status = forms.ChoiceField(choices=Product.STATUS_CHOICES,
                               widget=forms.RadioSelect())
    category = ModelChoiceField(Category.objects.all(), required=False,
                                empty_label=None)

    class Meta:
        model = Product
        fields = ('title', 'category', 'sub_a', 'sub_b', 'brand', 'status',
                  'contact_phone', 'whatsapp', 'contact_email', 'description',
                  'price',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FormProduct, self).__init__(*args, **kwargs)

        if 'category' in self.data:
            try:
                sub_a_id = int(self.data.get('id'))
                self.fields['sub_a'].queryset = SubA.objects.filter(
                    category_id=country_id
                )
            except (ValueError, TypeError):
                pass
        print(self)
        # elif self.instance.pk:
        #     self.fields['sub_a'].queryset = self.instance.country.city_set.order_by('name')

    def save(self, commit=True):
        instance = super(FormProduct, self).save(commit=False)
        instance.user = self.user

        if commit:
            instance.save()
        return instance


class FormImagesProduct(forms.ModelForm):

    class Meta:
        model = ImagesProduct
        fields = ('image',)

    def save(self, product, file, commit=True):
        instance = super(FormImagesProduct, self).save(commit=False)

        instance.product = product
        instance.image = file

        if commit:
            instance.save()
        return instance


class FormEditProduct(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('title', 'status', 'contact_phone', 'whatsapp',
                  'contact_email', 'description', 'price',)
