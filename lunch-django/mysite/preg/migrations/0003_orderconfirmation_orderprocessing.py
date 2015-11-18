# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preg', '0002_auto_20151115_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderconfirmation',
            name='OrderProcessing',
            field=models.BooleanField(default=False),
        ),
    ]
