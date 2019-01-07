# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

from product.models import Product

from .constants import (DELPRODUCT, MESSAGE_MOD, MESSAGE_USER, MODNOTIFICATION,
                        SUBJECT_MOD, SUBJECT_USER)
from .forms import FormReport
from .models import Report


@login_required
def report(request, product_id):
    if request.method == 'POST':
        try:
            existReport = Report.objects.get(product=product_id,
                                             reporter=request.user.id)
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
                product.count_report += 1
                report.save()
                product.save()
                # Verificacion sobre la cantidad de denuncias
                if MODNOTIFICATION <= product.count_report < DELPRODUCT:
                    send_mail(
                        SUBJECT_MOD,
                        MESSAGE_MOD + str(product.id),
                        settings.EMAIL_HOST_USER,
                        [settings.EMAIL_HOST_USER],
                        fail_silently=False
                    )
                elif product.count_report == DELPRODUCT:
                    delProduct(product_id)
                    send_mail(
                        SUBJECT_USER,
                        MESSAGE_USER,
                        settings.EMAIL_HOST_USER,
                        [product.user.email],
                        fail_silently=False
                    )
                return HttpResponse("Producto denunciado")
        else:
            # El usuario ya denuncio el producto
            return HttpResponse("No se puede volver a denunciar")
    else:
        product = Product.objects.get(id=product_id)
        return render(request, 'report.html', {'FormReport': FormReport,
                                               'product': product})


def delProduct(product_id):
    Product.objects.get(id=product_id).delete()
    return None
