# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CashMove',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('AmountMoney', models.FloatField()),
                ('DateCashMove', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('NameServis', models.CharField(max_length=30)),
                ('Telephone', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('DateOrder', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderConfirmation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Confirmation', models.BooleanField()),
                ('DateConfirmation', models.DateTimeField(null=True, blank=True)),
                ('ConfirmationOrderID', models.OneToOneField(to='preg.Order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProductLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('NumProduct', models.IntegerField()),
                ('Confirmation', models.BooleanField()),
                ('OrderID', models.ForeignKey(to='preg.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('NameProduct', models.CharField(max_length=30)),
                ('Price', models.FloatField()),
                ('DeliveryID', models.ForeignKey(to='preg.DeliveryService')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('NameCategory', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('balance', models.IntegerField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='ProductCategoryID',
            field=models.ForeignKey(to='preg.ProductCategory'),
        ),
        migrations.AddField(
            model_name='orderproductline',
            name='ProductID',
            field=models.ForeignKey(to='preg.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='UserID',
            field=models.ForeignKey(to='preg.UserProfile'),
        ),
        migrations.AddField(
            model_name='cashmove',
            name='UserCash',
            field=models.ForeignKey(to='preg.UserProfile'),
        ),
    ]
