# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Category, SubA, SubB, SubC


admin.site.register(Category)
admin.site.register(SubA)
admin.site.register(SubB)
admin.site.register(SubC)
