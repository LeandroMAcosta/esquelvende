# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=20, default="2945")
    avatar = models.ImageField(upload_to='avatar/',
                               default='avatar/default.jpg')
