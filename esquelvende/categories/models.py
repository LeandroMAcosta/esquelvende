# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Category(models.Model):
	category_name = models.CharField(max_length=100, null=True)
	def __str__(self):
		return self.category_name

class brands(models.Model):
	name_brands =  models.CharField(max_length=100, null=True)
	def __str__(self):
		return self.name_brands

class SubA(models.Model):
	category = models.ForeignKey(Category, null=True)
	brands = models.ManyToManyField(brands, blank=True)
	subA_name = models.CharField(max_length=100, null=True)
	def __str__(self):
		return self.subA_name


class SubB(models.Model):
	subA = models.ForeignKey(SubA, null=True)
	brands = models.ManyToManyField(brands, blank=True)
	subB_name = models.CharField(max_length=100, null=True)
	def __str__(self):
		return self.subB_name


class SubC(models.Model):
	subB = models.ForeignKey(SubB, null=True)
	brands = models.ManyToManyField(brands, blank=True)
	subC_name = models.CharField(max_length=100, null=True)
	def __str__(self):
		return self.subC_name
