# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from product.models import Product

from .constants import REASON_CHOICES


class Report(models.Model):
    product = models.ForeignKey(Product, related_name="report", null=True,
                                blank=True, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, related_name="reporter", null=True,
                                 blank=True, on_delete=models.CASCADE)
    reason = models.CharField(max_length=3, choices=REASON_CHOICES)
    description = models.TextField(blank=True)
