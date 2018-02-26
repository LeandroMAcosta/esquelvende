# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class LastSeen(models.Model):
	user = models.ForeignKey(User, blank=True)
	product = models.ForeignKey(Product)

	def __str__(self):
		return self.product.title