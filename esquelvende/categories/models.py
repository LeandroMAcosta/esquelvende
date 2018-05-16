# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class QuerySet(models.QuerySet):
    def class_name(self):
        return self.__class__.__name__


class QuerySetManager(models.Manager):

    def get_queryset(self):
        return QuerySet(self.model, using=self._db)

    def class_name(self):
        return self.get_queryset().class_name()


class Category(models.Model):
    objects = QuerySetManager()
    category_name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, null=True)

    def __str__(self):
        return self.category_name

    def class_name(self):
        return self.__class__.__name__


class Brand(models.Model):
    objects = QuerySetManager()
    brand_name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, null=True)

    def __str__(self):
        return self.brand_name

    def class_name(self):
        return self.__class__.__name__


class SubA(models.Model):
    objects = QuerySetManager()
    category = models.ForeignKey(Category, null=True)
    brand = models.ManyToManyField(Brand, blank=True)
    subA_name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, null=True)

    def __str__(self):
        return self.subA_name

    def class_name(self):
        return self.__class__.__name__


class SubB(models.Model):
    objects = QuerySetManager()
    subA = models.ForeignKey(SubA, null=True)
    brand = models.ManyToManyField(Brand, blank=True)
    subB_name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, null=True)

    def __str__(self):
        return self.subB_name

    def class_name(self):
        return self.__class__.__name__


class SubC(models.Model):
    subB = models.ForeignKey(SubB, null=True)
    brand = models.ManyToManyField(Brand, blank=True)
    subC_name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, null=True)

    def __str__(self):
        return self.subC_name
