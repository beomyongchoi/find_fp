# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-17 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_auto_20161117_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='description',
            field=models.TextField(max_length=5000),
        ),
    ]
