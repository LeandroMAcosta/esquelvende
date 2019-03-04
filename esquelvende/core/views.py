# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.contrib import messages

from forms import FormRegister, FormLogin
from utils import my_login
from product.models import Product, Favorite, History


def home(request):
    MAX_PRODUCTS = 2
    products = Product.objects.all().order_by('-id')[:MAX_PRODUCTS]
    context = {'products': products}
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        history = History.objects.filter(user=request.user)
        products_fav = [f.product for f in favorites]
        products_his = [h.product for h in history]
        context.update({'favorites': products_fav, 'history': products_his})

    return render(request, 'home.html', context)


def signup_user(request):
    if request.POST:
        form = FormRegister(request.POST)
        if form.is_valid():
            instance, password = form.save()
            return my_login(request, instance.username, password)
    else:
        form = FormRegister()
    context = {'form': form}
    return render(request, 'create_user.html', context)


def login_user(request):
    if request.POST:
        form = FormLogin(request.POST)
        if form.is_valid:
            username = request.POST['username']
            key = request.POST['password']
            access = authenticate(username=username, password=key)
            if access is not None:
                login(request, access)
                url = request.GET.get('next', '/')
                return redirect(url)
            else:
                messages.error(request, 'Usuario o contraseñas no validos')

    elif request.user.is_authenticated():
        return redirect('/')
    else:
        form = FormLogin()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('/login/')


def about_us(request):
    return render(request, 'about_us.html')
