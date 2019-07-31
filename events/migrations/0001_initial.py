# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-31 07:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('senders', '0002_auto_20190731_0650'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calendar_id', models.CharField(max_length=1024)),
                ('summary', models.TextField(blank=True, default='')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_events', to='senders.Sender')),
            ],
            options={
                'db_table': 'events',
                'ordering': ('start',),
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('calendar_id',)]),
        ),
    ]