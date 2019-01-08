from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.core.files import File
from django.urls import reverse
import urllib2
from urlparse import urlparse
from .models import Account


def get_avatar(backend, strategy, details, response, user=None, *args,
               **kwargs):
    if kwargs['is_new']:
        if backend.name == 'facebook':
            url = "http://graph.facebook.com/%s/picture?type=large"\
                  % response['id']
        if backend.name == 'google-oauth2':
            url = response['image'].get('url')
            url = url.replace("?sz=50", "?sz=200")

        name = urlparse(url).path.split('/')[-1]
        content = urllib2.urlopen(url)
        user.account.avatar.save(name, content, save=True)
