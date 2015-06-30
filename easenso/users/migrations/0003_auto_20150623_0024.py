# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150616_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='captcha',
            field=models.CharField(max_length=500),
        ),
    ]
