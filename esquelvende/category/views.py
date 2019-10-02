# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import JsonResponse

from .models import Category, SubA, SubB, Brand
from product.models import Product
from .abstract_category import AbstractCategory
import json


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


def categories(request):
    context = {'categories': Category.objects.all()}
    return render(request, 'categories.html', context)


def category(request, slug_category):
    category = get_object_or_404(Category, slug=slug_category)

    base = AbstractCategory(request, {'category': category})
    context = {
        'current_category': category,
        'products': base.resolve_products(),
        'quantity': base.resolve_quantity_products(),
        'path': base.resolve_path()
    }

    return render(request, 'base_category.html', context)


def sub_a(request, slug_category, slug_sub_a):
    sub_a = get_object_or_404(
        SubA,
        slug=slug_sub_a,
        category__slug=slug_category
    )

    base = AbstractCategory(request, {'category': sub_a.category, 'sub_a': sub_a})
    context = {
        'current_category': sub_a,
        'products': base.resolve_products(),
        'quantity': base.resolve_quantity_products(),
        'path': base.resolve_path()
    }

    return render(request, 'base_category.html', context)


def sub_b(request, slug_category, slug_sub_a, slug_sub_b):
    sub_b = get_object_or_404(
        SubB,
        slug=slug_sub_b,
        sub_a__slug=slug_sub_a,
        sub_a__category__slug=slug_category
    )

    base = AbstractCategory(
        request,
        {'category': sub_b.sub_a.category, 'sub_a': sub_b.sub_a, 'sub_b': sub_b}
    )
    context = {
        'current_category': sub_b,
        'products': base.resolve_products(),
        'quantity': base.resolve_quantity_products(),
        'path': base.resolve_path()
    }

    return render(request, 'base_category.html', context)


def products(request):
    base = AbstractCategory(request)
    context = {
        'categories': Category.objects.all(),
        'products': base.resolve_products(),
        'quantity': base.resolve_quantity_products()
    }

    return render(request, 'base_category.html', context)
