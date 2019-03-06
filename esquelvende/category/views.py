# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
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


# La view categories devuelve cada categoria con sus sub_a.
def categories(request):
    categories = Category.objects.all()
    res = {}

    for category in categories:
        res[category] = SubA.objects.filter(category=category)

    context = {'categories': res}
    return render(request, 'categories.html', context)


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
    search = request.GET.get('results', None)
    category = get_object_or_404(Category, slug=slug_category)

    filter_by = {'category__slug': category.slug}

    context = {'current_category': category,
               'categories': category.suba_set.all(),
               'products': Product.filter_products(search, filter_by)}
    return render(request, 'base_category.html', context)


"""
Las vistas sub_a y sub_b trabajan como si estuviera en la ruta
/categoria/slug_sub_a o .../sub_a/?brand=brand y
/categoria/slug_sub_a/slug_sub_b o .../slug_sub_b?brand=brand respectivamente.

Por conveniencia vimos que era mejor tratar a las marcas por GET y no
como las demas categorias.
"""


def sub_a(request, slug_category, slug_sub_a):
    search = request.GET.get('results', None)
    brand = request.GET.get('brand', None)
    context, filter_by = {}, {}

    category = get_object_or_404(Category, slug=slug_category)
    sub_a = get_object_or_404(
        SubA,
        slug=slug_sub_a,
        category__slug=slug_category
    )

    if brand:
        brand = get_object_or_404(Brand, slug=brand)
        filter_by['brand__slug'] = brand
        context['current_category'] = brand
    else:
        categories = sub_a.subb_set.all()
        if categories.exists():
            context['categories'] = categories
        else:
            # Al no encontrar sub_b relacionados entonces hay marcas.
            context['brands'] = sub_a.brand.all()
        context['current_category'] = sub_a

    filter_by.update({'category__slug': category.slug,
                      'sub_a__slug': sub_a.slug})
    context['products'] = Product.filter_products(search, filter_by)
    return render(request, 'base_category.html', context)


def sub_b(request, slug_category, slug_sub_a, slug_sub_b):
    search = request.GET.get('results', None)
    brand = request.GET.get('brand', None)
    context, filter_by = {}, {}

    category = get_object_or_404(Category, slug=slug_category)
    sub_a = get_object_or_404(
        SubA,
        slug=slug_sub_a,
        category__slug=slug_category
    )
    sub_b = get_object_or_404(SubB, slug=slug_sub_b, sub_a__slug=slug_sub_a)

    if brand:
        brand = get_object_or_404(Brand, slug=brand)
        filter_by['brand__slug'] = brand
        context['current_category'] = brand
    else:
        context.update({'brands': sub_b.brand.all(),
                        'current_category': sub_b})

    filter_by.update({'category__slug': category.slug,
                      'sub_a__slug': sub_a.slug,
                      'sub_b__slug': sub_b.slug})
    context['products'] = Product.filter_products(search, filter_by)
    return render(request, 'base_category.html', context)
