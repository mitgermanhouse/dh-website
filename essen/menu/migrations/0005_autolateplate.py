# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-29 20:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_lateplate_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoLatePlate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField()),
                ('days', models.TextField()),
            ],
        ),
    ]