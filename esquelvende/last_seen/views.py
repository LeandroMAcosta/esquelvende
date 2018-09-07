# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from products.models import Product

from .models import LastSeen


def add_last_seen(request, product):
    if request.user.is_authenticated:
        lastseen = LastSeen.objects.filter(user=request.user)
        list_product = [p.product for p in lastseen]
        if product not in list_product:
            if len(list_product) > 10:
                LastSeen.objects.filter(user=request.user).first().delete()
            LastSeen.objects.create(user=request.user, product=product)
    return None
