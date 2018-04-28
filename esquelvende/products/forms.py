from django import forms
from .models import Product, ImagesProduct


class FormProduct(forms.ModelForm):
	title = forms.CharField(max_length=30)
	def __init__(self, *args, **kwargs):
		super(FormProduct, self).__init__(*args, **kwargs)
		self.fields['category'].widget.attrs.update({'onChange': 'category_selector(event)'})
		self.fields['subA'].widget.attrs.update({'onChange': 'category_selector(event)', 'class':'selected'})
		self.fields['subB'].widget.attrs.update({'onChange': 'category_selector(event)', 'class':'selected'})
		self.fields['subC'].widget.attrs.update({'onChange': 'category_selector(event)', 'class':'selected'})
		self.fields['brands'].widget.attrs.update({'class':'selected'})
		

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
					'contact_email',
					'description',
					'price')


class FormImagesProduct(forms.ModelForm):
	image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

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
			'contact_email',
			'description',
			'price')