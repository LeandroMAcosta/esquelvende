from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from account.models import Account


def my_login(request, user_name, key):
    access = authenticate(username=user_name, password=key)
    if access is not None:
        login(request, access)
        url = request.GET.get('next') or reverse('inicio')
        return HttpResponseRedirect(url)
    else:
        return HttpResponse("Error al registrarse")


def create_profile(strategy, details, response, user, *args, **kwargs):
    if kwargs['is_new']:
        Account.objects.create(user=user)
    return kwargs
