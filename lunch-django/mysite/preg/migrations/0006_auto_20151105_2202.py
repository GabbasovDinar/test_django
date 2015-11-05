# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preg', '0005_auto_20151105_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashmove',
            name='UserCash',
            field=models.ForeignKey(to='preg.UserProfile'),
        ),
    ]
