from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=200)
    directions = models.TextField()
    serving_size = models.PositiveSmallIntegerField(validators = [MinValueValidator(1), MaxValueValidator(1000)])

    def __str__(self):
        return self.recipe_name


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)
    ingredient_name = models.CharField(max_length=100, null=True)
    units = models.CharField(max_length=30, null=True)
    quantity = models.FloatField(default=0, validators = [MinValueValidator(0)])

    def __str__(self):
        return self.ingredient_name
