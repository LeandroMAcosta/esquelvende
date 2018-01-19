# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Category(models.Model):
	category_name = models.CharField(max_length=100, null=True)
	def __str__(self):
		return self.category_name


class Subcategory(models.Model):
	category = models.ForeignKey(Category, null=True)
	subcategory_name = models.CharField(max_length=100, null=True)
	def __str__(self):
		return self.subcategory_name


class Filter(models.Model):
	subcategory = models.ForeignKey(Subcategory, null=True)
	filter_name = models.CharField(max_length=100, null=True)
	def __str__(self):
		return self.filter_name