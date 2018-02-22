# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Favorite(models.Model):
	user = models.ForeignKey(User, null=True)
	product = models.OneToOneField(Product)

	def __str__(self):
		product = Product.objects.get(id=self.id)
		return product.title