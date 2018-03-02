# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Category(models.Model):
	category_name = models.CharField(max_length=100, null=True)
	def __str__(self):
		return self.category_name


class SubA(models.Model):
	category = models.ForeignKey(Category, null=True)
	subA_name = models.CharField(max_length=100, null=True)
	def __str__(self):
		return self.subA_name


class SubB(models.Model):
	subA = models.ForeignKey(SubA, null=True)
	subB_name = models.CharField(max_length=100, null=True)
	def __str__(self):
		return self.subB_name


class SubC(models.Model):
	subB = models.ForeignKey(SubB, null=True)
	subC_name = models.CharField(max_length=100, null=True)
	def __str__(self):
		return self.subC_name
