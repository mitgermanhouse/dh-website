# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-01 20:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20190101_1958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeingredient',
            name='ingredient',
        ),
        migrations.RemoveField(
            model_name='recipeingredient',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='recipeingredient',
            name='units',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='quantity',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='units',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='ingredient_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='RecipeIngredient',
        ),
        migrations.DeleteModel(
            name='Unit',
        ),
    ]
