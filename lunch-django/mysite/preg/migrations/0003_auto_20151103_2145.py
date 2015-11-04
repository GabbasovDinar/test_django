# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preg', '0002_cashmove'),
    ]

    operations = [
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
                ('UserID', models.ForeignKey(to='preg.UserProfile')),
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
    ]
