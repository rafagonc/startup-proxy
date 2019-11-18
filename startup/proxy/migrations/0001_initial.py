# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-11-14 05:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('scale_resource_name', models.CharField(max_length=255)),
                ('scale_resource_type', models.CharField(max_length=255)),
                ('host', models.CharField(max_length=255)),
                ('resource_on', models.BooleanField(default=True)),
                ('suspend', models.BooleanField(default=False)),
                ('start_at', models.DateTimeField(null=True)),
                ('end_at', models.DateTimeField(null=True)),
            ],
        ),
    ]
