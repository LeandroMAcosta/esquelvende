# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse

from .models import Category, SubA, SubB, Brand
from product.models import Product


def load_categories(request):
    CATEGORY = 'id_category'
    SUBA = 'id_suba'
    SUBB = 'id_subb'

    if request.method == 'GET':
        data = {}
        query = None
        category_name = request.GET.get('category_name', None)
        id_category = request.GET.get('id_category', None)

        if category_name and id_category:
            if category_name == CATEGORY:
                query = SubA.objects.filter(category=id_category)
                data['id'] = 'suba'
            elif category_name == SUBA:
                query = SubB.objects.filter(sub_a=id_category)
                data['id'] = 'subb'
                if not query.exists():
                    query = Brand.objects.filter(suba__pk=id_category)
                    data['id'] = 'brand'
            elif category_name == SUBB:
                query = Brand.objects.filter(subb__pk=id_category)
                data['id'] = 'brand'
            else:
                pass

            for cat in query:
                data[cat.id] = str(cat)

        return JsonResponse(data)
