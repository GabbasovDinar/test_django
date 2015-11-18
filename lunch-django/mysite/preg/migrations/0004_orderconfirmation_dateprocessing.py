# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preg', '0003_orderconfirmation_orderprocessing'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderconfirmation',
            name='DateProcessing',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
