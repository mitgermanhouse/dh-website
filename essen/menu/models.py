from enum import Enum

from django.db import models
from django.db.models import Case, When, Value
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from home.models import Member
from recipes.models import Recipe


# -- MealDayTime --
class Weekday(Enum):
    SUN = 0, 'Sunday'
    MON = 1, 'Monday'
    TUE = 2, 'Tuesday'
    WED = 3, 'Wednesday'
    THU = 4, 'Thursday'
    FRI = 5, 'Friday'
    SAT = 6, 'Saturday'

    def __new__(cls, value, description=None):
        entry = object.__new__(cls) 
        entry._value_ = value
        entry._description_ = description
        return entry

    @property
    def description(self):
        return self._description_

class MealTime(Enum):
    BREAKFAST = 'BRK', 'Breakfast'
    BRUNCH = 'BRU', 'Brunch'
    LUNCH = 'LUN', 'Lunch'
    DINNER = 'DIN', 'Dinner'

    def __new__(cls, value, description=None):
        entry = object.__new__(cls) 
        entry._value_ = value
        entry._description_ = description
        return entry

    @property
    def description(self):
        return self._description_

class MealDayTime(models.Model):
    weekday = models.SmallIntegerField(choices=[(tag.value, tag.description) for tag in Weekday])
    meal_time = models.CharField(max_length=5, choices=[(tag.value, tag.description) for tag in MealTime])

    def __str__(self):
        return f'{Weekday(self.weekday).description} {MealTime(self.meal_time).description}'

# -- Other Models --
class Menu(models.Model):
    start_date = models.DateField('Start Date')
    servings = models.IntegerField(validators=[MinValueValidator(1)])
    notes = models.TextField(blank=True)

    @property
    def name(self):
        return self.start_date.strftime('Menu for %b %d, %Y')

    def __str__(self):
        return self.name


class Meal(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    meal_day_time = models.ForeignKey(MealDayTime, on_delete=models.PROTECT, null=True)

    recipes = models.ManyToManyField(Recipe)

    manual_lateplates = models.ManyToManyField(Member, related_name='manual_lateplate_meals', blank=True)
    deleted_auto_lateplates = models.ManyToManyField(Member, related_name='deleted_auto_lateplate_meals', blank=True)

    @property
    def name(self):
        return self.date.strftime(str(self.meal_day_time) + ' (%b %d, %Y)')

    @property
    def lateplates(self):
        alp_qs = self.meal_day_time.auto_lateplate_members.all()
        dalp_qs = self.deleted_auto_lateplates.all()
        mlp_qs = self.manual_lateplates.all()

        return (alp_qs.exclude(pk__in=dalp_qs) | mlp_qs).distinct()

    def __str__(self):
        return self.name

    meal_order = ('date', Case(
        When(meal_day_time__meal_time='BRK', then=Value(0)), 
        When(meal_day_time__meal_time='BRU', then=Value(1)),
        When(meal_day_time__meal_time='LUN', then=Value(2)),
        When(meal_day_time__meal_time='DIN', then=Value(3)),
        default = Value(100)
    ))


class MealRating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField(null=True)

