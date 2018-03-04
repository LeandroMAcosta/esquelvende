from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect
from .models import UserProfile
from users.models import User

def my_login(request, user_name, key):
	access = authenticate(username=user_name, password=key)
	if access is not None:
		login(request, access)
		url = request.GET.get('next') or reverse('inicio')
		return HttpResponseRedirect(url)
	else:
		return HttpResponse("Error al registrarse")


def create_profile(strategy, details, response, user, *args, **kwargs):
	email = details['email']
	user_object = User.objects.get(email=email)
	UserProfile.objects.create(user = user_object)
	return kwargs