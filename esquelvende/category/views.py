# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse

from .models import Category, SubA, SubB, Brand
from product.models import Product


def load_categories(request):
    CATEGORY, SUB_A, SUB_B = 'id_category', 'id_sub_a', 'id_sub_b'

    if request.method == 'GET':
        query, data = None, {}
        category = request.GET.get('category', None)
        id_category = request.GET.get('id_category', None)
        next_category = request.GET.get('next_category', None)
        """
        El id en data lo necesita el frontend para crear el select con el
        nombre del campo de la base de datos.
        """
        data['id'] = next_category

        if category and id_category:
            if category == CATEGORY:
                query = SubA.objects.filter(category=id_category)
            elif category == SUB_A:
                query = SubB.objects.filter(sub_a=id_category)
                if not query.exists():
                    query = Brand.objects.filter(suba__pk=id_category)
                    data['id'] = 'brand'
            elif category == SUB_B:
                query = Brand.objects.filter(subb__pk=id_category)

            if query:
                for cat in query:
                    data[cat.id] = str(cat)

        return JsonResponse(data)
