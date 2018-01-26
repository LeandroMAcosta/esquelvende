# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .forms import FormProduct, FormImagesProduct
from users.models import User
from .models import Product, ImagesProduct
from django.contrib.auth.decorators import login_required
from categories.models import Category, Subcategory, Filter


def home(request):
    return render(request, 'home.html', {})


@login_required(login_url='/login/')
def publish(request):
    if request.POST:
        form = FormProduct(request.POST)
        form_image = FormImagesProduct(request.POST, request.FILES)
        if form.is_valid() and form_image.is_valid():
            image_product = form_image.save(commit=False)
            category = Category.objects.get(pk=request.POST['category'])
            subcategory = Subcategory.objects.get(pk=request.POST['subcategory'])
            filter = Filter.objects.get(pk=request.POST['filter'])
            user_product = Product(
                                    user=request.user,
                                    title=request.POST['title'], 
                                    category=category, 
                                    subcategory=subcategory, 
                                    filter=filter,
                                    description=request.POST['description'], 
                                    price=request.POST['price']
                                    )
            user_product.save()
            # request.FILES is a dictionary 
            for image in request.FILES.getlist('image'):
                image_product = ImagesProduct.objects.create(
                                                              product=user_product,
                                                              image=image
                                                            )
                image_product.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("error")
    else:
        form = FormProduct()
        form_image = FormImagesProduct()
    return render(request, 'publish.html', {'form': form, 'form_image': form_image})

def product_view(request, id):
    product = Product.objects.get(pk=id)
    images = product.imagesproduct_set.all()
    return render(request, 'product.html', {'product': product, 'images': images})
