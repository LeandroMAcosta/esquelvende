# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
# from django.forms import modelformset_factory
from django.http import Http404, JsonResponse
from django.shortcuts import HttpResponse, redirect, get_object_or_404, render

# from hitcount.models import HitCount
# from hitcount.views import HitCountMixin

import constants
from category.models import Category, SubA, SubB, Brand
from .forms import FormEditProduct, FormImagesProduct, FormProduct
from .models import Product, ImagesProduct, Favorite, History
from account.views import user_products


def search(request):
    search = request.GET.get('results', None)

    if search is None:
        raise Http404

    try:
        filter_by = {}
        minim = request.GET.get('min', None)
        maxim = request.GET.get('max', None)
        if request.GET.get('cond', None):
            filter_by['status'] = request.GET.get('cond', None)

        if minim:
            filter_by['price__gte'] = int(minim)

        if maxim:
            filter_by['price__lte'] = int(maxim)

        products = Product.filter_products(search, filter_by)
        categories = Category.objects.all()
        context = {
            'categories': categories,
            'products': products,
            'quantity': len(products)
        }
        return render(request, 'base_category.html', context)
    except Exception as e:
        print(e)
        return redirect('/')


@login_required(login_url='/login/')
def publish_product(request):
    if request.method == 'POST':
        form = FormProduct(request.POST, user=request.user)
        if form.is_valid():
            images = request.POST.getlist('image')
            product = form.save()
            for count, id_file in enumerate(images):
                if count < constants.MAX_IMAGES:
                    try:
                        obj = ImagesProduct.objects.get(
                            pk=int(id_file),
                            product=product.pk
                        )
                        return HttpResponse(status=400)
                    except Exception:
                        obj = ImagesProduct.objects.get(pk=int(id_file))
                        obj.product = product
                        obj.save(product)
            return JsonResponse({"url": product.get_url()})

        data = {'err_code': constants.INVALID_FORM, 'err_msg': form.errors}
        return Response(data)
    else:
        form = FormProduct(initial={'contact_email': request.user.email})
        return render(request, './publish_product.html', {'form': form})


@login_required(login_url='/login/')
def upload_image(request):
    if request.method == 'POST':
        form = FormImagesProduct(request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('image')
            data = []
            for count, file in enumerate(images):
                tmp = {}
                if count < 6:
                    image = ImagesProduct.objects.create(image=file,)
                    tmp['id'] = image.id
                    tmp['url'] = image.thumbnail.name
                    data.append(tmp)
            return JsonResponse(data, safe=False)
        return HttpResponse(status=400)


@login_required(login_url='/login/')
def delete_product(request, product_id=None):
    product = get_object_or_404(Product, pk=product_id, user=request.user)
    if request.POST:
        try:
            product.delete_product()
        except Exception:
            return HttpResponse(status=400)
        return JsonResponse({'product_id': product.id})


@login_required(login_url='/login/')
def republish_product(request, product_id=None):
    product = get_object_or_404(
        Product.actives,
        pk=product_id,
        user=request.user
    )
    if request.POST:
        try:
            product.republish()
        except Exception:
            return HttpResponse(status=400)
        return user_products(request, './user_products/ajax_products.html')


def view_product(request, product_slug=None, product_id=None):
    product = get_object_or_404(
        Product.actives,
        slug=product_slug,
        pk=product_id,
    )

    context = {"product": product, "images": product.images.all()}

    if request.user.is_authenticated:
        History.add_to_history(request.user, product)
        context["has_favorite"] = Favorite.objects.filter(product=product.id,
                                                          user=request.user
                                                          ).exists()
    return render(request, './view_product.html', context)


def create_favorite(request, product_id=None):

    if request.POST:
        product = get_object_or_404(Product.actives, pk=product_id)
        if not request.user.is_authenticated:
            return JsonResponse(
                {'url': '/login/?next=/product/%s-%s/' % (product.slug, product.pk)}
            )
        try:
            favorite = Favorite.objects.get(
                product=product_id,
                user=request.user
            )
            favorite.delete()
        except Favorite.DoesNotExist:
            favorite = Favorite.objects.create(
                product=product,
                user=request.user
            )
            return HttpResponse(status=201)


# @login_required(login_url='/login/')
# def edit_product(request, product_id):
#     product = get_object_or_404(Product, pk=product_id, user=request.user)
#     ImagesFormSet = modelformset_factory(ImagesProduct,
#                                          fields=('product', 'image'),
# extra=0)
#     if request.POST:
#         form = FormEditProduct(request.POST, instance=product)
#         form_images = ImagesFormSet(request.POST, request.FILES,
#                                     queryset=product.imagesproduct_set.all())
#         if form.is_valid() and form_images.is_valid():
#             form.save()
#             form_images.save()
#         return redirect("/")
#     else:
#         form = FormEditProduct(instance=product)
#         form_images = ImagesFormSet(queryset=product.imagesproduct_set.all())
#     return render(request, 'edit_product.html', {'form': form,
#                                                  'form_images': form_images})
