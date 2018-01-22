# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import FormRegister
from .utils import my_login
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from products.urls import home

#import pdb; pdb.set_trace()

#Test para ver usuario actual conectado, borrar def, url y html mas adelante
#def test_login(request):
#	user = request.user
#	return render(request, 'test.html', {'user':user, 'test':request.resolver_match})

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
				return HttpResponseRedirect('/')
			else:
				return HttpResponse("error")
	else:
		form = AuthenticationForm()
	return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')
