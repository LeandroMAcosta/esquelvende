# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from .forms import FormProduct, FormImagesProduct
from users.models import User
from .models import Product, ImagesProduct
from django.contrib.auth.decorators import login_required
from categories.models import Category, Subcategory, Filter
from reports.forms import FormReport


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
            return HttpResponse("error")
    else:
        form = FormProduct()
        form_image = FormImagesProduct()
    return render(request, 'publish.html', {'form': form, 'form_image': form_image})


def product_view(request, id):
    product = get_object_or_404(Product, pk=id)
    images = product.imagesproduct_set.all()
    return render(request, 'product.html', {'product': product, 'images': images, 'FormReport': FormReport})


@login_required(login_url='/login/')
def delete_product(request, id):
    Product.objects.get(id=id, user=request.user).delete()
    return HttpResponseRedirect('/')
