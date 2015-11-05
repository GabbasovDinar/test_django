# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preg', '0004_auto_20151105_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashmove',
            name='UserCash',
            field=models.OneToOneField(to='preg.Order'),
        ),
    ]
