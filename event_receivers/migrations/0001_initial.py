# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-08-07 09:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventReceiver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opened', models.BooleanField(default=False)),
                ('clicked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_receiver_accounts', to='accounts.Account')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_receiver_events', to='events.Event')),
            ],
            options={
                'db_table': 'event_receivers',
                'ordering': ('id',),
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='eventreceiver',
            unique_together=set([('event', 'account')]),
        ),
    ]
