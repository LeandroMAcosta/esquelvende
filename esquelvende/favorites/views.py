# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import FavoriteForm
from products.models import Product
from .models import Favorite


@login_required(login_url='/login/')
def create_favorite(request, product_id):
	if request.method == 'POST':
		form = FavoriteForm(request.POST)
		if form.is_valid():
			try:
				existFavorite = Favorite.objects.get(product=product_id, user=request.user.id)
			except Favorite.DoesNotExist:
				existFavorite = None

			if existFavorite is None: 
				favorite = form.save(commit=False)
				product = Product.objects.get(id=product_id)
				favorite.user = request.user
				favorite.product = product
				favorite.save()
				return HttpResponse("guardado")
			else:
				existFavorite.delete()
				return HttpResponse("elimina3")
	else:
		form = FavoriteForm()
		return HttpResponse("GET")

