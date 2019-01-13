# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(Categories):
    pass


class Brand(Categories):
    pass


class SubA(Categories):
    category = models.ForeignKey(Category)
    brand = models.ManyToManyField(Brand)


class SubB(Categories):
    sub_a = models.ForeignKey(SubA)
    brand = models.ManyToManyField(Brand)
