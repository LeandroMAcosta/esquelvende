# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.forms import (UserChangeForm, UserCreationForm)

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	avatar = models.ImageField(upload_to='media/avatar')
	phone = models.IntegerField()


