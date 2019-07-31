# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-31 06:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=254)),
                ('password', models.CharField(max_length=50)),
                ('recovery_email', models.CharField(blank=True, default='', max_length=254)),
                ('phone_number', models.CharField(blank=True, default='', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_location', models.CharField(blank=True, default='', max_length=150)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(default='')),
            ],
            options={
                'db_table': 'senders',
                'ordering': ('id',),
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='sender',
            unique_together=set([('email', 'id')]),
        ),
    ]