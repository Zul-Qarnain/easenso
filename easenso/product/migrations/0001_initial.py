# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Featured',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_featured', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('price', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('warranty', models.DateField(null=True)),
                ('status', models.CharField(max_length=1, choices=[(b'B', b'Brand New'), (b'S', b'Second Hand')])),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product_Details',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color', models.CharField(max_length=30)),
                ('size', models.CharField(max_length=30)),
                ('model', models.CharField(max_length=30)),
                ('product', models.ForeignKey(to='product.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Product_Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('media', models.FileField(null=True, upload_to=b'product/media', blank=True)),
                ('caption', models.CharField(max_length=50)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sub_Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('category', models.ForeignKey(to='product.Category')),
            ],
        ),
        migrations.CreateModel(
            name='User_Rate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.CharField(max_length=1, choices=[(b'5', b'5 stars'), (b'4', b'4 stars'), (b'3', b'3 stars'), (b'2', b'2 stars'), (b'1', b'1 star')])),
                ('product', models.ForeignKey(to='product.Product')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VIP_Rate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.CharField(max_length=1, choices=[(b'5', b'5 stars'), (b'4', b'4 stars'), (b'3', b'3 stars'), (b'2', b'2 stars'), (b'1', b'1 star')])),
                ('product', models.ForeignKey(to='product.Product')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(to='product.Sub_Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='featured',
            name='product',
            field=models.ForeignKey(to='product.Product'),
        ),
    ]
