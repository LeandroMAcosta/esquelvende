# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-19 17:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='filter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Filter'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Subcategory'),
        ),
    ]
