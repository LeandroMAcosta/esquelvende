# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	phone = models.IntegerField(default=None, null=True)
	avatar = models.ImageField(upload_to='avatar/', default='avatar/default.jpg')
