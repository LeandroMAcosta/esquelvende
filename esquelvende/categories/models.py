# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from managers import QuerySet, QuerySetManager


class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, null=True)
    objects = QuerySetManager()

    def __str__(self):
        return self.name

    def class_name(self):
        return self.__class__.__name__


class Sub(models.Model):
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, null=True)
    objects = QuerySetManager()

    # No crea un tabla en db.
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def class_name(self):
        return self.__class__.__name__


class SubA(Sub):
    category = models.ForeignKey(Category, null=True)
    brand = models.ManyToManyField(Brand, blank=True)


class SubB(Sub):
    subA = models.ForeignKey(SubA, null=True)
    brand = models.ManyToManyField(Brand, blank=True)


class Brand(models.Model):
    pass
