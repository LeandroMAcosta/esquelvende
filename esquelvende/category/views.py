# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
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
        obj['id'] = 'branCadaCadads'

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
    # TODO: Esta view devuelve las categorias con sus sub_a.
    pass


"""
IMPORTANTE.

Las siguientes views, retornan por contexto
1) Ubicacion actual
2) Productos
3) Categorias o marcas o nada

Para el 1er elemento si se encuentra en /electrodomestico/telefonos/
la ubicacion actual es telefonos.

Para el 2do elemento, los productos son filtrados por search o solo
por las categorias en el caso de que no exista search o bien ambos.

Para el 3er elemento.
- Retornar categorias sigifica que la ubicacion actual tiene o bien sub_a
  o sub_b como hijos.
- Retornar marcas quiere decir que un sub_a, tiene hijos pero son marcas y
  lo mismo para un sub_b.
- No retornar categorias o marcas significa que la ubicacion
  actual no tiene hijos relacionados.
"""


def category(request, slug_category):
    category = get_object_or_404(Category, slug=slug_category)
    search = request.GET.get('results', None)

    filter_by = {'category__slug': category.slug}
    products = Product.filter_products(search, filter_by)

    categories = category.suba_set.all()

    context = {'categories': categories, 'products': products,
               'current_category': category}
    template = 'base_category.html'
    return render(request, template, context)


def sub_a(request, slug_category, slug_sub_a):
    """
    Esta view trabaja como si estuviera en la ruta
    /categoria/slug_sub_a o /categoria/slug_sub_a?brand=brand.

    Por conveniencia vimos que era mejor tratar a las marcas por GET y no
    como las demas categorias.
    """
    search = request.GET.get('results', None)
    brand = request.GET.get('brand', None)
    context = {}
    filter_by = {}

    category = get_object_or_404(Category, slug=slug_category)
    sub_a = get_object_or_404(
        SubA,
        slug=slug_sub_a,
        category__slug=slug_category
    )
    filter_by.update({'category__slug': category.slug,
                      'sub_a__slug': sub_a.slug})

    if brand:
        brand = get_object_or_404(Brand, slug=brand)
        filter_by['brand__slug'] = brand
        context['current_category'] = brand
    else:
        categories = sub_a.subb_set.all()
        if categories.exists():
            context['categories'] = categories
        else:
            """
            Si no encontramos subcategorias de una sub_a
            entonces tiene marcas relacionadas.
            """
            brands = sub_a.brand.all()
            context['brands'] = brands

        context['current_category'] = sub_a

    products = Product.filter_products(search, filter_by)
    context['products'] = products

    template = 'base_category.html'
    return render(request, template, context)


def sub_b(request, slug_category, slug_sub_a, slug_sub_b):
    """
    Esta view trabaja como si estuviera en la ruta
    /categoria/slug_sub_a/slug_sub_b o
    /categoria/slug_sub_a/slug_sub_b?brand=brand.
    """
    search = request.GET.get('results', None)
    brand = request.GET.get('brand', None)
    context = {}
    filter_by = {}

    category = get_object_or_404(Category, slug=slug_category)
    sub_a = get_object_or_404(
        SubA,
        slug=slug_sub_a,
        category__slug=slug_category
    )
    sub_b = get_object_or_404(SubB, slug=slug_sub_b, sub_a__slug=slug_sub_a)
    filter_by.update({'category__slug': category.slug,
                      'sub_a__slug': sub_a.slug,
                      'sub_b__slug': slug_sub_b.slug})

    if brand:
        brand = get_object_or_404(Brand, slug=brand)
        filter_by['brand__slug'] = brand
        context['current_category'] = brand
    else:
        brands = sub_b.brand.all()
        context.update({'brands': brands, 'current_category': sub_b})

    products = Product.filter_products(search, filter_by)
    context['products'] = products

    template = 'base_category.html'
    return render(request, template, context)
