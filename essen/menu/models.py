# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from recipes.models import Recipe


# Create your models here.

# TODO: Add validators
class Menu(models.Model):
    start_date = models.DateField("Start Date")
    servings = models.IntegerField(default=24)
    notes = models.TextField()

    def __str__(self):
        return self.start_date.strftime("Menu for %b %d, %Y")


class Meal(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    meal_name = models.CharField(max_length=200, default="Sunday Brunch")

    recipes = models.ManyToManyField(Recipe)
    #recipes.clear() and recipes.remove(___) are valid

    def __str__(self):
        return self.date.strftime(self.meal_name + " for %b %d, %Y")

    @property
    def day(self):
        # TODO: Turn into enum model field
        for i, d in enumerate(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]):
            if d in self.meal_name:
                return i

        return 0

    @property
    def time(self):
        # TODO: Turn into enum model field
        for i, t in enumerate(["Breakfast", "Brunch", "Lunch", "Dinner"]):
            if t in self.meal_name:
                return i

        return 0


class LatePlate(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, null=True)
    name = models.TextField(null=True)

    def __str__(self):
        return self.name


class AutoLatePlate(models.Model):
    username = models.TextField() # TODO: Migrate to user reference
    days = models.TextField(default="")
    dietary = models.TextField(default="")

    def __str__(self):
        return self.username + " " + self.days

class MealRating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    username = models.TextField() # TODO: Migrate to user reference
    rating = models.IntegerField(null=True) # TODO: Add min and max value validators
    comment = models.TextField(null=True)

