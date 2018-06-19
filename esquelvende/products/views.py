# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import Http404, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, render)
from django.utils import timezone
from hitcount.models import HitCount
from hitcount.views import HitCountMixin

from categories.models import Brand, Category, SubA, SubB
from last_seen.models import LastSeen
from last_seen.views import add_last_seen
from reports.forms import FormReport
from users.models import User

from .forms import FormEditProduct, FormImagesProduct, FormProduct
from .models import ImagesProduct, Product
from .utils import json_selector


def product_filter(search):
    return Product.objects.filter(Q(title__istartswith=search) |
                                  Q(title__contains=search) |
                                  Q(title__iendswith=search))


def home(request):
    query = Category.objects.all()
    search = request.GET.get('search')
    if search:
        products = product_filter(search)
        return render(request, 'category_parser/category_parser.html',
                      {'query': query, 'search_products': products})
    return render(request, 'home.html', {'categories': query})


@login_required(login_url='/login/')
def user_products(request):
    query = Product.objects.filter(user=request.user, enable=True)
    return render(request, 'list_products.html', {'user_products': query})


def product_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if not product.is_expired():
        # Agrega Lastseen
        add_last_seen(request, product)
        images = product.imagesproduct_set.all()
        hit_count = HitCount.objects.get_for_object(product)
        hit_count_response = HitCountMixin.hit_count(request, hit_count)
        return render(request, 'product_view.html', {'product': product,
                                                     'images': images})
    raise Http404


@login_required(login_url='/login/')
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id, user=request.user)
    if request.POST:
        product.enable = False
        product.save()
        return HttpResponseRedirect("/")
    return render(request, 'delete_product.html', {'product': product})


@login_required(login_url='/login/')
def republish(request, product_id):
    product = get_object_or_404(Product, pk=product_id, user=request.user)
    if request.POST:
        product.enable = True
        product.published_date = timezone.now()
        product.save()
        return HttpResponseRedirect("/productos/")
    return render(request, 'republish.html', {'product': product})


@login_required(login_url='/login/')
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id, user=request.user)
    ImagesFormSet = modelformset_factory(ImagesProduct,
                                         fields=('product', 'image'), extra=0)
    if request.POST:
        form = FormEditProduct(request.POST, instance=product)
        form_images_set = ImagesFormSet(
                                    request.POST, request.FILES,
                                    queryset=product.imagesproduct_set.all())
        if form.is_valid() and form_images_set.is_valid():
            form.save()
            form_images_set.save()
        return HttpResponseRedirect("/")
    else:
        form = FormEditProduct(instance=product)
        form_images_set = ImagesFormSet(
                                    queryset=product.imagesproduct_set.all())
    return render(request,
                  'edit_product.html',
                  {'form': form,
                   'form_images_set': form_images_set})


@login_required(login_url='/login/')
def publish(request):
    if (request.GET.get('id_generic') is not None and
            request.GET.get('value_generic') is not None):
        if request.GET.get('id_generic') == 'id_category':
            return json_selector(request.GET.get('value_generic'),
                                 'id_category',
                                 request.GET.get('value_generic'))
        elif request.GET.get('id_generic') == 'id_subA':
            return json_selector(request.GET.get('value_generic'),
                                 'id_subA',
                                 request.GET.get('value_generic'))
        elif request.GET.get('id_generic') == 'id_subB':
            return json_selector(request.GET.get('value_generic'),
                                 'id_subB',
                                 request.GET.get('value_generic'))
    if request.POST:
        form = FormProduct(request.POST)
        form_image = FormImagesProduct(request.POST, request.FILES)
        if form.is_valid() and form_image.is_valid():
            image_product = form_image.save(commit=False)
            obj_product = form.save(commit=False)
            obj_product.user = request.user
            obj_product.published_date = timezone.now()
            obj_product.save()
            # request.FILES is a dictionary
            for cont, image in enumerate(request.FILES.getlist('image')):
                if cont < 6:
                    image_product = ImagesProduct.objects.create(
                                    product=obj_product, image=image)
                    image_product.save()
            return HttpResponseRedirect('/')
    else:
        form = FormProduct(initial={'contact_email': request.user.email})
        form_image = FormImagesProduct()
    return render(request, 'publish.html', {'form': form,
                                            'form_image': form_image})


def categories(request, slug_category=None, slug_suba=None, slug_subb=None):
    id_brand = request.GET.get('i_b')
    search = request.GET.get('search')
    query_products = None
    if not(slug_category or slug_suba or slug_subb or id_brand):
        query = Category.objects.all()
        return render(request, 'category_parser/categories.html',
                      {'query': query})
    elif slug_category and not (slug_suba or slug_subb or id_brand):
        if not Category.objects.filter(slug=slug_category).exists():
            raise Http404
        obj = Category.objects.get(slug=slug_category)
    elif slug_category and slug_suba and id_brand and not slug_subb:
        if not (Category.objects.filter(slug=slug_category, suba__slug=slug_suba).exists() and
                SubA.objects.filter(brand__id=id_brand).exists()):
            raise Http404
        obj = Brand.objects.get(id=id_brand)
    elif slug_category and slug_suba and not (slug_subb or id_brand):
        if not Category.objects.filter(slug=slug_category, suba__slug=slug_suba).exists():
            raise Http404
        obj = SubA.objects.get(category__slug=slug_category, slug=slug_suba)
    elif slug_category and slug_suba and slug_subb and id_brand:
        if not(Category.objects.filter(slug=slug_category, suba__slug=slug_suba).exists() and
               SubA.objects.filter(subb__slug=slug_subb).exists() and
               SubB.objects.filter(brand__id=id_brand).exists()):
            raise Http404
        obj = Brand.objects.get(id=id_brand)
    elif slug_category and slug_suba and slug_subb and not id_brand:
        if not(Category.objects.filter(slug=slug_category, suba__slug=slug_suba).exists() and
               SubA.objects.filter(subb__slug=slug_subb).exists()):
            raise Http404
        obj = SubB.objects.get(subA__slug=slug_suba, slug=slug_subb)
    else:
        raise Http404

    list_dict = [{'category__slug': slug_category},
                 {'subA__slug': slug_suba},
                 {'subB__slug': slug_subb},
                 {'brands__id': id_brand}]

    if search:
        query_products = Product.objects.all()
        for dict in list_dict:
            if dict.values()[0] is not None:
                query_products = query_products.filter(
                                        Q(title__contains=search, **dict) |
                                        Q(title__istartswith=search, **dict) |
                                        Q(title__iendswith=search, **dict))
    return render(
        request,
        'category_parser/category_parser.html',
        {'object': obj, 'search_products': query_products})
