# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse

def login_view(request):
	if request.POST:
		form = AuthenticationForm(request.POST)
		if form.is_valid:
			user_name = request.POST['username']
			key = request.POST['password']
			access = authenticate(request, username=user_name, password=key)
			if access is not None:
				login(request, access)
				return HttpResponseRedirect(reverse(""))
			else:
				return HttpResponse("error")
	else:
		form = AuthenticationForm()
	return render(request, 'login.html', {'form': form})