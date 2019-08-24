# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-07-29 19:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20190708_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagesproduct',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.Product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]