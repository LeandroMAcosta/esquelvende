from django import forms

from django.forms import ModelChoiceField
from .models import ImagesProduct, Product, Favorite

from django.core.exceptions import ValidationError
from category.models import Category, SubA, SubB, Brand


class FormProduct(forms.ModelForm):
    status = forms.ChoiceField(choices=Product.STATUS_CHOICES,
                               widget=forms.RadioSelect())
    category = ModelChoiceField(Category.objects.all(), empty_label=None)

    class Meta:
        model = Product
        fields = ('title', 'category', 'sub_a', 'sub_b', 'brand', 'status',
                  'contact_phone', 'whatsapp', 'contact_email', 'description',
                  'price',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FormProduct, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(FormProduct, self).clean()
        category = cleaned_data.get('category')
        sub_a = cleaned_data.get('sub_a')
        sub_b = cleaned_data.get('sub_b')
        brand = cleaned_data.get('brand')

        error_0 = {'category': 'Complete las categorias faltantes.'}
        error_1 = {'category': 'Elija una opcion correcta.'}

        if category and sub_a and sub_b and brand:
            try:
                obj = SubB.objects.get(name=sub_b, brand=brand.id)
            except Exception as e:
                raise forms.ValidationError(error_1,)
        elif category and sub_a and sub_b:
            try:
                obj = SubB.objects.get(name=sub_b, sub_a=sub_a.id)
                if obj.brand.all().count():
                    raise forms.ValidationError(error_0,)
            except Exception as e:
                raise forms.ValidationError(error_1,)
        elif category and sub_a and brand:
            try:
                obj = SubA.objects.get(name=sub_a, brand=brand)
            except Exception as e:
                raise forms.ValidationError(error_1,)
        elif category and sub_a:
            try:
                obj = SubA.objects.get(category=category.id, pk=sub_a.id)
                if (obj.brand.all().count() or obj.subb_set.all().count()):
                    raise forms.ValidationError(error_0,)
            except Exception as e:
                raise forms.ValidationError(error_1,)
        elif category:
            if category.suba_set.all().count() and sub_a is None:
                raise forms.ValidationError(error_0,)

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

        try:
            obj = ImagesProduct.objects.get(pk=instance.pk)
            instance = ImagesProduct.objects.create(
                product=product,
                image=file
            )
        except Exception as e:
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
