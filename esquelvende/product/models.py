# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator

from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin

from category.models import Brand, Category, SubA, SubB
from search import get_query
import constants

# Para trabajar con las imagenes.
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
import sys
import os


class ProductInactivesManager(models.Manager):
    def get_queryset(self):
        return super(ProductInactivesManager, self).get_queryset().filter(
            updated_at__date__lt=timezone.now() - timedelta(days=30),
            is_deleted=False
        )


class ProductActivesManager(models.Manager):
    def get_queryset(self):
        return super(ProductActivesManager, self).get_queryset().filter(
            updated_at__date__gt=timezone.now() - timedelta(days=30),
            is_deleted=False
        )

    def custom_filter(self, search=None, filter_by=None):
        fields = ['title', 'category__slug', 'sub_a__slug', 'brand__slug',
                  'sub_b__slug']
        query = get_query(search, fields, filter_by)
        products = self.filter(query)
        return products


class Product(models.Model, HitCountMixin):
    STATUS_CHOICES = (
        ('U', 'Usado'),
        ('N', 'Nuevo')
    )

    title = models.CharField(max_length=50, default=None)
    slug = models.SlugField()  # Title + id
    description = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    count_report = models.IntegerField(default=0)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(Category, null=True, blank=True)
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
    hit_count = GenericRelation(
        HitCount,
        object_id_field='object_pk',
        related_query_name='hit_count_relation',
    )
    price = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )
    updated_at = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    actives = ProductActivesManager()
    inactives = ProductInactivesManager()
    objects = models.Manager()

    def __str__(self):
        return self.title

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


class ImagesProduct(models.Model):
    product = models.ForeignKey(
        Product,
        null=True,
        blank=True,
        related_name='images'
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
            ftype = constants.CHECK_EXTENSION[file_ext]
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
        new_img.paste(image, ((base_width-heigth)/2, (base_width-weight)/2))
        return new_img


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    @classmethod
    def add_to_history(cls, user, product):
        try:
            obj = Product.actives.get(user=user, pk=product.id)
        except Product.DoesNotExist:
            _, created = cls.objects.get_or_create(
                user=user,
                product=product
            )

            if created:
                histories = cls.objects.filter(user=user)
                if histories.count() >= constants.MAX_HISTORY:
                    histories[0].delete()

    def __str__(self):
        return self.product.title
