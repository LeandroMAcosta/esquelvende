# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
# from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, render

from .constants import *
from category.models import Category, SubA, SubB, Brand
from .forms import FormEditProduct, FormImagesProduct, FormProduct
from .models import Product, ImagesProduct, Favorite, History
from account.views import user_products


@login_required(login_url='/login/')
def publish_product(request):
    if request.method == 'POST':
        form = FormProduct(request.POST, user=request.user)
        if form.is_valid():
            images = request.POST.getlist('image')
            product = form.save()
            for count, id_file in enumerate(images):
                if count < MAX_IMAGES:
                    try:
                        obj = ImagesProduct.objects.get(
                            pk=int(id_file),
                            product=product.pk
                        )
                        return HttpResponse(status=400)
                    except ImagesProduct.DoesNotExist:
                        obj = ImagesProduct.objects.get(pk=int(id_file))
                        obj.product = product
                        obj.save(product)
            return JsonResponse({"url": product.get_url()})

        data = {'err_code': constants.INVALID_FORM, 'err_msg': form.errors}
        return Response(data)
    else:
        form = FormProduct(initial={'contact_email': request.user.email})
        return render(request, 'publish_product.html', {'form': form})


@login_required(login_url='/login/')
def upload_product_image(request):
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
def delete_product(request, pk=None):
    product = get_object_or_404(Product.actives, pk=pk, user=request.user)
    if request.method == 'POST':
        try:
            product.delete_product()
        except Exception:
            return HttpResponse(status=400)
        return JsonResponse({'product_id': product.id})


@login_required(login_url='/login/')
def republish_product(request, pk=None):
    product = get_object_or_404(Product.actives, pk=pk, user=request.user)
    if request.method == 'POST':
        try:
            product.republish()
        except Exception:
            return HttpResponse(status=400)
        return user_products(request, './user_products/ajax_products.html')


def product_detail(request, slug=None, pk=None):
    product = get_object_or_404(Product.actives, slug=slug, pk=pk)

    has_favorite = None
    if request.user.is_authenticated:
        has_favorite = product.favorites.filter(user=request.user).exists()

    context = {
        "product": product,
        "images": product.images.all(),
        "has_favorite": has_favorite,
        # TODO: published: Mostrar hace cuanto esta publicado.
        # TODO: status: Mostrar el estado del producto.
        # TODO: path: Mostrar la ruta de categorias del producto.
    }


    return render(request, 'view_product.html', context)


def favorite_product(request, pk=None):
    if request.method == 'POST':
        product = get_object_or_404(Product.actives, pk=pk)
        if not request.user.is_authenticated:
            return JsonResponse(
                {'url': '/login/?next={}'.format(product.get_url())}
            )

        favorite, created = product.favorites.get_or_create(user=request.user)
        if not created:
            favorite.delete()
            return HttpResponse(status=200)
        return HttpResponse(status=201)


def history_product(request, pk=None):
    if request.method == 'POST':
        product = get_object_or_404(Product.actives, pk=pk)
        if not request.user.is_authenticated:
            return JsonResponse(
                {'url': '/login/?next={}'.format(product.get_url())}
            )

        History.add_to_history(request.user, product)
        return HttpResponse(status=200)


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
