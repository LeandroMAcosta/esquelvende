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
	if request.POST:
		form = FavoriteForm(request.POST)
		if form.is_valid():
			try:
				existFavorite = Favorite.objects.get(product=product_id, user=request.user)
			except Favorite.DoesNotExist:
				existFavorite = None
			if existFavorite is None: 
				favorite = form.save(commit=False)
				product = Product.objects.get(pk=product_id)
				favorite.user = request.user
				favorite.product = product
				favorite.save()
			else:
				existFavorite.delete()
	else:
		form = FavoriteForm()
		return HttpResponse("No valido")


@login_required(login_url='/login/')
def list_favorites(request):
	favorites = Favorite.objects.filter(user=request.user)
	return render(request, 'favorites.html', {'favorites': favorites})