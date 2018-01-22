# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .forms import FormProduct
from users.models import User
from .models import Product
from django.contrib.auth.decorators import login_required
from categories.models import Category, Subcategory, Filter



def home(request):
    return render(request, 'home.html', {})


@login_required(login_url='/login/')
def publish(request):
    if request.POST:
        form = FormProduct(request.POST)
        if form.is_valid:
            user = User.objects.get(pk=request.user.id)
            category = Category.objects.get(pk=request.POST['category'])
            subcategory = Subcategory.objects.get(pk=request.POST['subcategory'])
            filter = Filter.objects.get(pk=request.POST['filter'])
            user_product = Product(
                                    user=user,
                                    title=request.POST['title'], 
                                    category=category, 
                                    subcategory=subcategory, 
                                    filter=filter,
                                    description=request.POST['description'], 
                                    price=request.POST['price']
                                    )
            user_product.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("error")
    else:
        form = FormProduct()
    return render(request, 'publish.html', {'form': form})