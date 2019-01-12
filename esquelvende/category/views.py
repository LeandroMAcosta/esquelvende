# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse

from .models import Category, SubA, SubB, Brand
from product.models import Product


def get_categories(idx, value):
    obj = {}
    if idx == 'id_category':
        query = SubA.objects.filter(category=value)
        obj['id'] = 'subA'
    elif idx == 'id_subA':
        query = SubB.objects.filter(subA=value)
        obj['id'] = 'subB'
    else:
        query = Brand.objects.filter(subb__pk=value)
        obj['id'] = 'brands'

    if not query.exists() and idx == 'id_subA':
        query = Brand.objects.filter(suba__pk=value)
        obj['id'] = 'brands'

    for category in query:
        obj[category.id] = str(category)
    return JsonResponse(obj)


def tree_categories(request):
    if request.method == 'GET':
        idx = request.GET.get('id')
        value = request.GET.get('value')
        if idx and value:
            if idx == 'id_category':
                return get_categories('id_category', value)
            elif idx == 'id_subA':
                return get_categories('id_subA', value)
            elif idx == 'id_subB':
                return get_categories('id_subB', value)
            else:
                return JsonResponse({})


def load_sub_a(request):
    category_id = request.GET.get('id')
    sub_a = SubA.objects.filter(category_id=category_id)
    return render(request, 'sub_a.html', {'sub_a': sub_a})
