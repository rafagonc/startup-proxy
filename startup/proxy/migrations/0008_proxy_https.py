# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-11-17 03:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0007_auto_20191116_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='proxy',
            name='https',
            field=models.BooleanField(default=True),
        ),
    ]
