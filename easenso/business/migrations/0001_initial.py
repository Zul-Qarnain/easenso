# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('mobile_number', models.CharField(max_length=30)),
                ('tel_number', models.CharField(max_length=30)),
                ('logo', models.FileField(null=True, upload_to=b'business/logo', blank=True)),
                ('background', models.FileField(null=True, upload_to=b'business/background', blank=True)),
                ('email', models.EmailField(max_length=254)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Business_Products',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('business', models.ForeignKey(to='business.Business')),
                ('product', models.ForeignKey(to='product.Product')),
            ],
        ),
    ]
