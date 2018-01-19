# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from categories.models import Category, Subcategory, Filter


class Product(models.Model):
	title = models.CharField(max_length=50)
	user = models.ForeignKey('auth.User')
	category = models.ForeignKey(Category)
	subcategory = models.ForeignKey(Subcategory)
	filter = models.ForeignKey(Filter, null=True)
	description	= models.TextField()
	price = models.IntegerField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
	
	def __str__(self):
		return self.title

    #def publish(self):
    #	self.published_date = timezone.now()	
    #    self.save 