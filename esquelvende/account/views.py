# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import FormAvatar, FormEditAccount, FormEditUser
from .models import Account
from category.models import Category
from product.models import History, Favorite, Product


@login_required(login_url='/login/')
def edit_user(request):
    user = request.user
    user_info = Account.objects.get(user=user)
    query = Category.objects.all()
    if request.POST:
        form = FormEditUser(request.POST, instance=user)
        form_profile = FormEditAccount(request.POST, instance=user_info)
        form_avatar = FormAvatar(
            request.POST, request.FILES, instance=user_info)

        if form.is_valid():
            form.save()

        if form_avatar.is_valid() and request.FILES.get('avatar', False):
            form_avatar.save(commit=False)
            form_avatar.avatar = request.FILES['avatar']
            form_avatar.save()

        if form_profile.is_valid():
            form_profile.save()
            # profile = form_profile.save(commit=False)
            # profile.phone = 20
            # profile.save()

        return redirect(reverse('edit_user'))
    else:
        form = FormEditUser(instance=user)
        form_avatar = FormAvatar(instance=user_info)
        form_profile = FormEditAccount(instance=user_info)
        context = {'form': form, 'form_avatar': form_avatar,
                   'form_profile': form_profile, 'categories': query}
        return render(request, 'edit_user.html', context)


class HistoryList(LoginRequiredMixin, ListView):
    model = History
    template_name = 'list_history.html'
    paginate_by = 30

    def get_queryset(self):
        return History.filter_products(self.request.user)


class Favorites(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'list_favorites.html'
    paginate_by = 30

    def get_queryset(self):
        return Favorite.filter_products(self.request.user)


@login_required(login_url='/login/')
def user_products(request, template=None):
    """
    No filtramos productos por active=True porque ademas queremos
    los que no estan activos.
    Tambien, vemos si alguno supero el limite de publicacion y lo actulizamos.
    """
    products = [
        product
        for product in Product.objects.filter(user=request.user, delete=False)
        if product.is_expired() or not product.is_expired()  # Skip (update products)
    ]

    context = {'products': products}
    template = template or './user_products/list_of_products.html'

    return render(request, template, context)
