# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-21 20:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('care_point', '0005_auto_20181221_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decision',
            name='charge',
            field=models.DecimalField(decimal_places=2, max_digits=6, max_length=30),
        ),
        migrations.AlterField(
            model_name='decision',
            name='hours',
            field=models.DecimalField(decimal_places=2, max_digits=6, max_length=4),
        ),
        migrations.AlterField(
            model_name='decision',
            name='percent_payment',
            field=models.DecimalField(decimal_places=2, max_digits=6, max_length=5),
        ),
        migrations.AlterField(
            model_name='decision',
            name='ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='care_point.Ward'),
        ),
    ]
