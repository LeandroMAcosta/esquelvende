# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from hitcount.models import HitCount, HitCountMixin

from categories.models import Brand, Category, SubA, SubB

from .constants import STATUS_CHOICES


class Product(models.Model, HitCountMixin):
    description = models.TextField()
    contact_email = models.EmailField()
    title = models.CharField(max_length=30)
    enable = models.BooleanField(default=True)
    delete = models.BooleanField(default=False)
    count_report = models.IntegerField(default=0)
    category = models.ForeignKey(Category, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    subA = models.ForeignKey(SubA, null=True, blank=True)
    subB = models.ForeignKey(SubB, null=True, blank=True)
    whatsapp = models.CharField(max_length=50, null=True)
    brands = models.ForeignKey(Brand, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    contact_phone = models.CharField(max_length=50, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, null=True,
                              blank=True)
    hit_count = GenericRelation(HitCount, object_id_field='object_pk',
                                related_query_name='hit_count_relation')
    price = models.PositiveIntegerField(default=0,
                                        validators=[MinValueValidator(0)])

    def __str__(self):
        return self.title

    # True si el producto expiro
    def is_expired(self):
        return timezone.now() > (self.published_date + timedelta(days=30))


class ImagesProduct(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to='products/', blank=True)
