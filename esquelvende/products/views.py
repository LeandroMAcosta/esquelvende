# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from .forms import FormProduct, FormImagesProduct
from users.models import User
from .models import Product, ImagesProduct
from django.contrib.auth.decorators import login_required
from categories.models import Category, Subcategory, Filter
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from last_seen.models import LastSeen
from django.http import Http404
from django.forms import modelformset_factory


def home(request):

	return render(request, 'home.html', {})


@login_required(login_url='/login/')
def publish(request):
	if request.POST:
		form = FormProduct(request.POST)
		form_image = FormImagesProduct(request.POST, request.FILES)
		if form.is_valid() and form_image.is_valid():
			image_product = form_image.save(commit=False)
			obj_product = form.save(commit=False)
			obj_product.user = request.user
			obj_product.save()
			# request.FILES is a dictionary 
			for cont, image in enumerate(request.FILES.getlist('image')):
				if cont < 6:
					image_product = ImagesProduct.objects.create(product=obj_product, image=image)
					image_product.save()
			return HttpResponseRedirect('/')
	else:
		form = FormProduct(initial={'contact_email': request.user.email})
		form_image = FormImagesProduct()
	return render(request, 'publish.html', {'form': form, 'form_image': form_image})


def product_view(request, product_id):
	query_product = Product.objects.filter(pk=product_id).not_expired()
	product = query_product.first()
	if request.user.is_authenticated:
		lastseen = LastSeen.objects.filter(user=request.user)   #List of LastSeen objects
		list_product = [ p.product for p in lastseen]           #List of Products objects
		if product not in list_product:
			if len(list_product) > 10:
				LastSeen.objects.all().first().delete()
			LastSeen.objects.create(user=request.user, product=product)

	if product:
		images = product.imagesproduct_set.all()
		hit_count = HitCount.objects.get_for_object(product)
		hit_count_response = HitCountMixin.hit_count(request, hit_count)
		return render(request, 'product_view.html', {'product': product, 'images': images})
	raise Http404 


@login_required(login_url='/login/')
def delete_product(request, product_id):
	product = get_object_or_404(Product, pk=product_id, user=request.user)
	if request.POST:
		product.delete()
		return HttpResponseRedirect("/")
	else:
		return render(request, 'delete_product.html', {'product': product})


@login_required(login_url='/login/')
def edit_product(request, product_id):
	product = get_object_or_404(Product, pk=product_id, user=request.user)
	ImagesFormSet = modelformset_factory(ImagesProduct, fields=('product', 'image'), extra=0)
	if request.POST:
		form = FormProduct(request.POST, instance=product)
		form_images_set = ImagesFormSet(request.POST, request.FILES, queryset=product.imagesproduct_set.all())
		if form.is_valid() and form_images_set.is_valid():
			form.save()
			form_images_set.save()
		return HttpResponseRedirect("/")
	else:
		form = FormProduct(instance=product)
		form_images_set = ImagesFormSet(queryset=product.imagesproduct_set.all())
	return render(request, 'edit_product.html', {'form': form, 'form_images_set': form_images_set})

	
@login_required(login_url='/login/')
def list_products(request): 
	products_not_expired = Product.objects.filter(user=request.user).not_expired()
	products_expired = Product.objects.filter(user=request.user).expired()
	return render(request,'list_products.html', {'products_expired': products_expired, 'products_not_expired': products_not_expired})
