# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Brand, Category, SubA, SubB, SubC

admin.site.register(Category, Brand, SubA, SubB, SubC)
