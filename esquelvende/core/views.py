# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import FormRegister, FormLogin
from .utils import my_login
from product.models import Product, Favorite, History


def home(request):
    MAX_PRODUCTS = 10
    products = Product.actives.order_by('-id')[:MAX_PRODUCTS]
    context = {'products': products}
    if request.user.is_authenticated:
        context['favorites'] = Product.actives.filter(favorite__user=request.user.pk)
        context['history'] = Product.actives.filter(history__user=request.user.pk)
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
    return render(request, 'login_and_signup/signup.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.POST:
        form = FormLogin(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            access = authenticate(username=username, password=password)
            if access is not None:
                login(request, access)
                return redirect(request.GET.get('next', '/'))
            else:
                messages.error(
                    request,
                    'Usuario o contraseña mal ingresado.'
                )
    else:
        form = FormLogin()
    return render(request, 'login_and_signup/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('/login/')


def about_us(request):
    return render(request, 'about_us.html')


def faq(request):
    return render(request, 'faq.html')
