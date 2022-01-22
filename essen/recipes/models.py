from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    directions = models.TextField()
    serving_size = models.PositiveSmallIntegerField(validators = [MinValueValidator(1), MaxValueValidator(1000)])

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255, null=True)
    unit = models.CharField(max_length=127, null=True)
    quantity = models.FloatField(default=0, validators = [MinValueValidator(0)])
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
