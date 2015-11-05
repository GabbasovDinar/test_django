# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preg', '0003_auto_20151103_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashmove',
            name='UserCash',
            field=models.ForeignKey(to='preg.Order'),
        ),
    ]
