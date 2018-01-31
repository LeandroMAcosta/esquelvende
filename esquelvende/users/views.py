# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import FormRegister
from .forms import FormEditUser
from .utils import my_login
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from products.urls import home


@login_required(login_url='/login/')
def edit_user(request):
	user = request.user
	if request.POST:
		form = FormEditUser(request.POST, instance = user)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/")
	else:
		form = FormEditUser(instance = user)
	return render(request, 'edit_user.html', {'form': form})


def new_user(request):
    if request.POST:
        form = FormRegister(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            key = form.cleaned_data.get('password')
            user.set_password(key)
            form.save()
            return my_login(request, username, key)
    else:
        form = FormRegister()
    return render(request, 'create_user.html', {'form': form})

def login_view(request):
	if request.POST:
		form = AuthenticationForm(request.POST)
		if form.is_valid:
			username = request.POST['username']
			key = request.POST['password']
			access = authenticate(request, username=username, password=key)
			if access is not None:
				login(request, access)
				return HttpResponseRedirect(request.GET.get('next'))
			else:
				return HttpResponse("Error al loguearse")
	elif request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		form = AuthenticationForm()
	return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')
