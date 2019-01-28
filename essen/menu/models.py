# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime, timedelta
from django.utils.encoding import python_2_unicode_compatible
from recipes.models import Recipe


# Create your models here.

@python_2_unicode_compatible
class Menu(models.Model):
    start_date = models.DateField("Start Date")
    servings = models.IntegerField(default=24)
    notes = models.TextField()

    def __str__(self):
        return self.start_date.strftime("Menu for %b %d, %Y")


@python_2_unicode_compatible
class Meal(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    meal_name = models.CharField(max_length=200, default="Sunday Brunch")

    recipes = models.ManyToManyField(Recipe)
    #recipes.clear() and recipes.remove(___) are valid

    def __str__(self):
        return self.date.strftime(self.meal_name + " for %b %d, %Y")


@python_2_unicode_compatible
class LatePlate(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, null=True)
    name = models.TextField(null=True)

    def __str__(self):
        return self.name

