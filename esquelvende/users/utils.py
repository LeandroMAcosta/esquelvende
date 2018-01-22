from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect


def my_login(request, user_name, key):
    access = authenticate(username=user_name, password=key)
    if access is not None:
        login(request, access)
        return HttpResponseRedirect(reverse("/"))
    else:
        return HttpResponse("Error")
