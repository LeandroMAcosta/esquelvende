from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect
from .models import UserProfile
from users.models import User

from urlparse import urlparse
import urllib2
from django.core.files import File

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
		UserProfile.objects.create(user = user)
	return kwargs

def get_avatar(backend, strategy, details, response,
				user=None, *args, **kwargs):
	if kwargs['is_new']:
		if backend.name == 'facebook':
			url = "http://graph.facebook.com/%s/picture?type=large"%response['id']
		if backend.name == 'google-oauth2':
			url = response['image'].get('url')

		name = urlparse(url).path.split('/')[-1]
		content = urllib2.urlopen(url)
		user.userprofile.avatar.save(name, content, save=True)