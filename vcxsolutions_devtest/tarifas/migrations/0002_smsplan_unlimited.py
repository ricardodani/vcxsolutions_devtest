# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 20:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarifas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsplan',
            name='unlimited',
            field=models.BooleanField(default=False, verbose_name='Ilimitados'),
        ),
    ]