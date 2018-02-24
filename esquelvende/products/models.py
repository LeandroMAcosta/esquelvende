# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from categories.models import Category, Subcategory, Filter
from django.core.validators import MinValueValidator


class Product(models.Model):
	title = models.CharField(max_length=50)
	description	= models.TextField()
	contact_phone = models.CharField(max_length=50, null=True)
	contact_email = models.EmailField()
	price = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
	count_report = models.IntegerField(default=0)
	category = models.ForeignKey(Category, null=True)
	filter = models.ForeignKey(Filter, null=True)
	subcategory = models.ForeignKey(Subcategory, null=True)
	user = models.ForeignKey(User, blank=True, null=True)

	def __str__(self):
		return self.title


class ImagesProduct(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to='products/')

