# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
from .models import Product, ImagesProduct
from reports.constants import SUBJECT_USER, MESSAGE_USER


def delete_product_report(modeladmin, request, queryset):
    for query in queryset:
        Product.objects.get(id=query.id).delete()
        send_mail(
            SUBJECT_USER,
            MESSAGE_USER,
            settings.EMAIL_HOST_USER,
            [query.user.email],
            fail_silently=False
        )
    return None

delete_product_report.short_description = 'Eliminar producto reportado'


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['id']
    actions = [delete_product_report]
    
admin.site.register(Product, ProductAdmin)
admin.site.register(ImagesProduct)
