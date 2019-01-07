# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from .forms import FormAvatar, FormEditAccount, FormEditUser
from .models import Account
from category.models import Category


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

