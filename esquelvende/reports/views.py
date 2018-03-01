# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Report
from .forms import FormReport
from .constants import MODNOTIFICATION, DELPRODUCT
from products.models import Product


@login_required
def report(request, product_id):
    if request.method == 'POST':
        try:
            existReport = Report.objects.get(product=product_id, reporter=request.user.id)
        except Report.DoesNotExist:
            existReport = None

        if not existReport:
            # El usuario no denuncio el producto
            form = FormReport(request.POST)
            if form.is_valid():
                reporter = request.user
                product = Product.objects.get(id=product_id)
                report = form.save(commit=False)
                report.reporter = reporter
                report.product = product
                product.count_report = product.count_report + 1
                report.save()
                product.save()

                # Verificacion sobre la cantidad de denuncias
                if MODNOTIFICATION <= product.count_report < DELPRODUCT:
                    notificationModerator(product_id)
                elif product.count_report == DELPRODUCT:
                    delProduct(product_id)
                return HttpResponse("Producto denunciado")
        else:
            # El usuario ya denuncio el producto
            return HttpResponse("No se puede volver a denunciar")
    else:
        form = FormReport()
        return HttpResponse("GET")


def notificationModerator(product_id):
    pass


def delProduct(product_id):
    Product.objects.get(id=product_id).delete()
    return None
