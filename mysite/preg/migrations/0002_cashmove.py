# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('preg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashMove',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('AmountMoney', models.FloatField()),
                ('DateCashMove', models.DateTimeField(default=django.utils.timezone.now)),
                ('UserCash', models.ForeignKey(to='preg.UserProfile')),
            ],
        ),
    ]
