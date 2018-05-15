# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.IntegerField(default=None, null=True)
    avatar = models.ImageField(upload_to='avatar/',
                               default='avatar/default.jpg')
