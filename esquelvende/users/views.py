# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.contrib import messages

from products.urls import home
from users.models import User

from .forms import FormAvatar, FormEditUserProfile, FormEditUser, FormRegister, FormLogin
from .models import UserProfile
from categories.models import Category
from .utils import my_login


@login_required(login_url='/login/')
def edit_user(request):
    user = request.user
    user_info = UserProfile.objects.get(user=user)
    query = Category.objects.all()
    if request.POST:
        form = FormEditUser(request.POST, instance=user)
        form_profile = FormEditUserProfile(request.POST, instance=user)
        form_avatar = FormAvatar(
            request.POST, request.FILES, instance=user_info)

        if form.is_valid():
            form.save()
        if form_avatar.is_valid() and request.FILES.get('avatar', False):
            form_avatar.save(commit=False)
            form_avatar.avatar = request.FILES['avatar']
            form_avatar.save()
        if form_profile.is_valid():
            form_profile.save()
        return HttpResponseRedirect(reverse('edit_user'))
    else:
        form = FormEditUser(instance=user)
        form_avatar = FormAvatar(instance=user_info)
        form_profile = FormEditUserProfile(instance=user_info)
    return render(request, 'edit_user.html', {'form':         form,
                                              'form_avatar':  form_avatar,
                                              'form_profile': form_profile,
                                              'categories':   query})


def new_user(request):
    if request.POST:
        form = FormRegister(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            key = form.cleaned_data.get('password')
            user.set_password(key)
            form.save()
            obj_user = User.objects.get(username=user)
            UserProfile.objects.create(user=obj_user)
            return my_login(request, username, key)
    else:
        form = FormRegister()
    return render(request, 'create_user.html', {'form': form})


def login_view(request):
    if request.POST:
        form = FormLogin(request.POST)
        if form.is_valid:
            username = request.POST['username']
            key = request.POST['password']
            access = authenticate(username=username, password=key)
            if access is not None:
                login(request, access)
                url = request.GET.get('next') or reverse('inicio')
                return HttpResponseRedirect(url)
            else:
                messages.error(request, 'Usuario o contraseñas no validos')

    elif request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        form = FormLogin()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')
