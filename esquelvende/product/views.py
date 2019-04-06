# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import Http404, JsonResponse
from django.shortcuts import HttpResponse, redirect, get_object_or_404, render

from hitcount.models import HitCount
from hitcount.views import HitCountMixin

from category.models import Category, SubA, SubB, Brand
from reports.forms import FormReport
from .forms import FormEditProduct, FormImagesProduct, FormProduct
from .models import Product, ImagesProduct, Favorite, History
from account.views import user_products


def search(request):
    search = request.GET.get('results', None)

    if search is None:
        raise Http404

    try:
        products = Product.filter_products(search)
        categories = Category.objects.all()
        context = {'categories': categories, 'products': products}
        return render(request, 'search.html', context)
    except Exception as e:
        return redirect('/')


def view_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id, active=True)
    if product.is_expired():
        raise Http404

    """
    Cada vez que un usuario hecha un vistazo a
    un producto se agrega a su historial.
    """
    if request.user.is_authenticated:
        try:
            # Para que un usuario no tenga sus productos en su historial.
            obj = Product.objects.get(user=request.user, pk=product_id)
        except Exception as e:
            History.add_to_history(request.user, product)

    images = product.imagesproduct_set.all()
    hit_count = HitCount.objects.get_for_object(product)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    context = {'product': product, 'images': images}
    return render(request, './view_product.html', context)


@login_required(login_url='/login/')
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id, user=request.user)
    if request.POST:
        product.delete_product()

        # Llama a la view user_products que devuelve los productos del usuario.
        return user_products(request, './user_products/ajax_products.html')


@login_required(login_url='/login/')
def republish_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id, user=request.user)
    if request.POST:
        product.republish()

        # Llama a la view user_products que devuelve los productos del usuario.
        return user_products(request, './user_products/ajax_products.html')


@login_required(login_url='/login/')
def create_favorite(request, product_id):
    if request.POST:
        product = get_object_or_404(Product, pk=product_id)
        try:
            favorite = Favorite.objects.get(
                product=product_id,
                user=request.user
            )
            if favorite:
                favorite.delete()

        except Exception as e:
            favorite = Favorite.objects.create(
                product=product,
                user=request.user
            )

        return HttpResponse(status=200)


@login_required(login_url='/login/')
def publish_product(request):
    if request.method == 'POST':
        form = FormProduct(request.POST, user=request.user)
        second_form = FormImagesProduct(request.FILES)
        if form.is_valid() and second_form.is_valid():
            product = form.save()
            files = request.FILES.getlist('image')
            """
            Contamos hasta 6 porque por ahora solo nos interesa
            guardar esa cantidad de imagenes, (deberia ser
            una constante).
            """
            for count, file in enumerate(files):
                if count < 6:
                    second_form.save(product, file)

            return JsonResponse({'id_product': product.id})
        else:
            data = {'err_code': 'invalid_form', 'err_msg': form.errors, }
            return JsonResponse(data)
    else:
        data = {'contact_email': request.user.email}
        form = FormProduct(initial=data)
        second_form = FormImagesProduct()

        context = {'form': form, 'form_images': second_form}
        return render(request, './publish_product.html', context)


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
