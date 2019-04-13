# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin

from category.models import Brand, Category, SubA, SubB
from search import get_query


class Product(models.Model, HitCountMixin):
    STATUS_CHOICES = (
        ('U', 'Usado'),
        ('N', 'Nuevo')
    )

    title = models.CharField(max_length=30, default=None)
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

    def is_expired(self):
        return timezone.now() > (self.updated_at + timedelta(days=30))

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
    image = models.ImageField(upload_to='product/', blank=True)


class Favorite(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)

    @classmethod
    def filter_products(cls, user):  # Devuelve productos activos y no vencidos.
        favorites = cls.objects.filter(user=user)
        products = [
            f.product
            for f in favorites
            if not f.product.is_expired() and f.product.active
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
            if not h.product.is_expired() and h.product.active
        ]
        return products

    def __str__(self):
        return self.product.title
