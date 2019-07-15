# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.template.defaultfilters import slugify
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin

from category.models import Brand, Category, SubA, SubB
from search import get_query

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
import sys
import os


class Product(models.Model, HitCountMixin):
    STATUS_CHOICES = (
        ('U', 'Usado'),
        ('N', 'Nuevo')
    )

    title = models.CharField(max_length=50, default=None)
    slug = models.SlugField()  # Title + id
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    # Cambiar este nombre delete creo que jode al delete() de django is_deleted
    delete = models.BooleanField(default=False)
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
    whatsapp = models.CharField(max_length=50, null=True, blank=True)
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
    updated_at = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def is_expired(self):
        expired = timezone.now() > (self.updated_at + timedelta(days=30))
        if expired:
            self.active = False
            self.save()
        return expired

    def delete_product(self):
        """
            Un producto eliminado no se mostrara a ningun usuario, es como
            si no existiera, pero lo guardamos por razones.
        """
        self.delete = True
        self.active = False
        self.save()

    def republish(self):
        if self.is_expired():
            self.active = True
            self.updated_at = timezone.now()
            self.save()

    @classmethod
    def filter_products(cls, search=None, filter_by=None):

        fields = ['title', 'category__slug', 'sub_a__slug', 'brand__slug',
                  'sub_b__slug']
        query = get_query(search, fields, filter_by)
        products = cls.objects.filter(query)
        return products


class ImagesProduct(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to='images/', blank=True)
    thumbnail = models.ImageField(upload_to='images/thumbnail', blank=True)

    def save(self, *args, **kwargs):
        # Redimensionar self.image
        self.image = self.handle_file(600)
        # Generamos thumbnail
        self.handle_file(180, True)
        super(ImagesProduct, self).save(*args, **kwargs)

    def handle_file(self, base_width, thumbnail=None):
        # Abrir la imagen cargada.
        im = Image.open(self.image)

        # Modificamos la imagen
        im.thumbnail((base_width, base_width), Image.ANTIALIAS)

        filename, file_ext = os.path.splitext(self.image.name)
        file_ext = file_ext.lower()

        # Obtenemos alto y ancho
        heigth = im.size[0]
        weight = im.size[1]

        # Creamos una imagen cuadrada y le pegaromos la del usuario.
        new_img = Image.new('RGB', (base_width, base_width), "white")
        new_img.paste(im, ((base_width-heigth)/2, (base_width-weight)/2))
        im = new_img

        if thumbnail:
            filename = filename.replace('images/', '')

        full_filename = filename + file_ext

        if file_ext in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif file_ext == '.gif':
            FTYPE = 'GIF'
        elif file_ext == '.png':
            FTYPE = 'PNG'
        else:
            raise Exception('Extesion incorrecta.')

        # Despues de modificarlo, lo guardamos en la salida.
        output = BytesIO()
        im.save(output, format=FTYPE, quality=100)
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


class Favorite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    @classmethod
    def filter_products(cls, user):  # Devuelve productos activos y no vencidos.
        favorites = cls.objects.filter(user=user)
        products = [
            f.product
            for f in favorites
            if not f.product.is_expired() and not f.product.delete
        ]
        return products

    def __str__(self):
        return self.product.title


class History(models.Model):
    MAX_HISTORY = 10  # Numero max. de historial por usuario.

    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)

    @classmethod
    def add_to_history(cls, user, product):
        _, created = cls.objects.get_or_create(
            user=user,
            product=product
        )

        if created:
            histories = cls.objects.filter(user=user)
            if histories.count() >= cls.MAX_HISTORY:
                histories[0].delete()

    @classmethod
    def filter_products(cls, user):  # Devuelve productos activos y no vencidos.
        history = cls.objects.filter(user=user)
        products = [
            h.product
            for h in history
            if not h.product.is_expired() and not h.product.delete
        ]
        return products

    def __str__(self):
        return self.product.title
