# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-03-02 17:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('councilmatic_core', '0035_bill_html_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jurisdiction',
            fields=[
                ('ocd_id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=300)),
                ('classification', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=2000)),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='jurisdiction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='organizations', to='councilmatic_core.Jurisdiction'),
        ),
    ]
