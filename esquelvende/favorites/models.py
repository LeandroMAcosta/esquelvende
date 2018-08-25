# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Favorite(models.Model):
    user = models.ForeignKey(User, null=True)
    product = models.OneToOneField(Product)

    def __str__(self):
        return self.product.title+" de "+self.user.username
