# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-08-07 11:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20190807_1152'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='override',
            options={'managed': True, 'verbose_name': 'Override', 'verbose_name_plural': 'Overrides'},
        ),
    ]