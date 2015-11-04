# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lunch', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='DatePublished',
        ),
        migrations.AlterField(
            model_name='order',
            name='DateOrder',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
