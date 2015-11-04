# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
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
                ('DateOrder', models.DateTimeField(verbose_name=b'date order product')),
                ('DatePublished', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProductLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('NumProduct', models.IntegerField()),
                ('Confirmation', models.BooleanField()),
                ('OrderID', models.ForeignKey(to='lunch.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('NameProduct', models.CharField(max_length=30)),
                ('Price', models.FloatField()),
                ('DeliveryID', models.ForeignKey(to='lunch.DeliveryService')),
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
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('NameUser', models.CharField(max_length=100)),
                ('SurnameUser', models.CharField(max_length=100)),
                ('Login', models.CharField(max_length=100)),
                ('Email', models.EmailField(max_length=100)),
                ('Password', models.CharField(max_length=100)),
                ('RegistrationDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('Authority', models.CharField(max_length=10)),
                ('Balance', models.FloatField()),
                ('RegistrationCheck', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='ProductCategoryID',
            field=models.ForeignKey(to='lunch.ProductCategory'),
        ),
        migrations.AddField(
            model_name='orderproductline',
            name='ProductID',
            field=models.ForeignKey(to='lunch.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='UserID',
            field=models.ForeignKey(to='lunch.User'),
        ),
        migrations.AddField(
            model_name='cashmove',
            name='UserCash',
            field=models.ForeignKey(to='lunch.User'),
        ),
    ]
