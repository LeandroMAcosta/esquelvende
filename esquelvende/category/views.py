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


def categories(request):
    pass


def category(request, slug_category):
    category = Category.objects.get_or_404(slug=slug_category)
    search = request.GET.get('results', None)

    # TODO: Completar parametros filter_products()
    filter_by = {'category__name': category.name}
    products = Product.filter_products(search, filter_by)

    categories = SubA.objects.filter(
        slug=slug_category,
        slug__suba=slug_sub_a
    )

    context = {'categories': categories, 'products': products}
    template = 'base_category.html'
    return render(request, template, context)


def sub_a(request, slug_category, slug_sub_a):
    suba = SubA.objects.get_or_404(
        slug=slug_sub_a,
        slug__category=slug_category
    )

    # TODO: Completar parametros filter_products()
    products = Product.filter_products()

    categories = SubB.objects.filter(
        slug__category=slug_category,
        slug__suba=slug_sub_a
    )

    """
        Si no encontramos subcategorias de una suba
        entonces tiene marcas relacionadas.
    """
    if not categories.exists():
        categories = Brand.objects.filter(
            slug__category=slug_category,
            slug__suba=slug_sub_a
        )

    context = {'categories': categories, 'products': products}
    template = 'base_category.html'
    return render(request, template, context)


def sub_b():
    pass
