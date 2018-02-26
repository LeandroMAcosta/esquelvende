# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from categories.models import Category, Subcategory, Filter
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta

class ProductQuerySet(models.QuerySet):
    def not_expired(self):
        return self.filter(created_date__gte= datetime.today() - timedelta(days=30))
    def expired(self):
    	return self.filter(created_date__lte= datetime.today() - timedelta(days=30))

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    def not_expired(self):
        return self.get_queryset().not_expired()
    def expired(self):
        return self.get_queryset().expired()


class Product(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
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

