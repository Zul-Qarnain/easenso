# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150623_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
