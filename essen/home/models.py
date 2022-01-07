from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from menu.models import MealDayTime

# Create your models here.

class DietaryRestriction(models.Model):
    long_name  = models.CharField(max_length=200)
    short_name = models.CharField(max_length=100)

class Member(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    class_year = models.IntegerField(null=True, validators=[MinValueValidator(2000), MaxValueValidator(2100)])
    major = models.CharField(max_length=20, null=True)
    bio = models.TextField(null=True)
    image = models.ImageField(upload_to="images/", null=True)

    auto_lateplates = models.ManyToManyField(MealDayTime, blank=True)
    dietary_restrictions = models.ManyToManyField(DietaryRestriction, blank=True)

    def __str__(self):
        return self.user.get_full_name()