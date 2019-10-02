# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator

from django.contrib.contenttypes.fields import GenericRelation

from category.models import Brand, Category, SubA, SubB
from .search import get_query
from .constants import *

# Para trabajar con las imagenes.
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
import sys
import os


class ProductInactivesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            updated_at__date__lt=timezone.now() - timedelta(days=30),
            is_deleted=False
        )


class ProductActivesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            updated_at__date__gt=timezone.now() - timedelta(days=30),
            is_deleted=False
        )

    def custom_filter(self, search=None, filter_by=None):
        # Retrun queryset or empty list
        fields = ['title', 'category__slug', 'sub_a__slug', 'brand__slug',
                  'sub_b__slug']
        query = get_query(search, fields, filter_by)
        if query:
            products = self.filter(query)
        else:
            products = self.all()
        return products


class Product(models.Model):
    STATUS_CHOICES = (
        ('U', 'Usado'),
        ('N', 'Nuevo')
    )
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    count_report = models.IntegerField(default=0)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    sub_a = models.ForeignKey(
        SubA,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    sub_b = models.ForeignKey(
        SubB,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    brand = models.ForeignKey(
        Brand,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    whatsapp = models.CharField(max_length=13, null=True, blank=True)
    contact_phone = models.CharField(max_length=50, null=True, blank=True)
    contact_email = models.EmailField()
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        null=True,
        blank=True,
    )
    price = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )
    updated_at = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    actives = ProductActivesManager()
    inactives = ProductInactivesManager()

    def is_expired(self):
        return timezone.now() > (self.updated_at + timedelta(days=30))

    def delete_product(self):
        self.is_deleted = True
        self.save()

    def republish(self):
        if self.is_expired():
            self.updated_at = timezone.now()
            self.save()

    def get_url(self):
        return reverse("product_detail", args=(self.slug, self.id))

    def __str__(self):
        return self.title


class ImagesProduct(models.Model):
    product = models.ForeignKey(
        Product,
        null=True,
        blank=True,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='images/', blank=True)
    thumbnail = models.ImageField(upload_to='images/thumbnail', blank=True)

    def save(self, product=None, *args, **kwargs):
        if product is None:
            self.image = self.handle_file(600)
            self.handle_file(180, True)
        super(ImagesProduct, self).save(*args, **kwargs)

    def handle_file(self, base_width, thumbnail=None):
        img = Image.open(self.image)
        img.thumbnail((base_width, base_width), Image.ANTIALIAS)
        img = self.standardize_image(img, base_width)

        filename, file_ext = os.path.splitext(self.image.name)
        file_ext = file_ext.lower()

        if thumbnail:
            filename = filename.replace('images/', '')

        full_filename = filename + file_ext

        try:
            ftype = CHECK_EXTENSION[file_ext]
        except KeyError:
            raise ('Wrong extension.')

        output = BytesIO()
        img.save(output, format=ftype, quality=100)
        output.seek(0)

        if thumbnail is None:
            # Cambiar image para que sea el valor de la imagen recien modificada.
            self.image = InMemoryUploadedFile(
                output,
                'ImageField',
                "%s" % full_filename,
                'image/jpeg',
                sys.getsizeof(output),
                None
            )
            return self.image
        else:
            self.thumbnail.save(
                full_filename,
                ContentFile(output.read()),
                save=False
            )
            output.close()

    def standardize_image(self, image, base_width):
        heigth, weight = image.size[0], image.size[1]
        new_img = Image.new('RGB', (base_width, base_width), "white")
        new_img.paste(image, (int((base_width-heigth)/2), int((base_width-weight)/2)))
        return new_img


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        related_name='favorites',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.product.title


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    @classmethod
    def add_to_history(cls, user, product):
        if product.user.pk != user.pk:
            _, created = product.history_set.get_or_create(
                user=user,
                product=product
            )
            if created:
                history = product.history_set.filter(user=user)
                if history.count() >= MAX_HISTORY:
                    history[0].delete()

    def __str__(self):
        return self.product.title
