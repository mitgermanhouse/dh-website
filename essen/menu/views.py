# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views import generic
from models import Menu
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime, timedelta
from recipes.models import Recipe
from .models import Menu, Meal, LatePlate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.


def index(request, date='None'):
    template_name = 'menu/index.html'
    context_object_name = 'menu'

    if datetime.utcnow().today().weekday() < 6:
        days_from_sunday = 1 + datetime.utcnow().today().weekday()
    else:
        days_from_sunday = 0
    target_date = datetime.utcnow() - timedelta(days=days_from_sunday)
    y, m, d = target_date.year, target_date.month, target_date.day
    menu = Menu.objects.filter(start_date__year=y,
                                start_date__month=m,
                                start_date__day=d).first()
    date = date.encode('utf-8')
    if date != 'None':
        target_date = datetime.strptime(date, '%m/%d/%Y')
        y, m, d = target_date.year, target_date.month, target_date.day
        menu = Menu.objects.filter(start_date__year=y,
                                   start_date__month=m,
                                   start_date__day=d).first()


    return render(request, template_name, {context_object_name: menu, 'target_date': target_date})


def add_menu(request):
    template_name = "menu/add_menu.html"
    context_object_name = 'recipe_choices'

    recipe_choices = Recipe.objects.all()

    return render(request, template_name, {context_object_name: recipe_choices})


def submit_menu(request):
    days_to_num = {"Sunday Brunch": 0, "Sunday Dinner": 0, "Monday Dinner": 1, "Tuesday Dinner": 2,
                   "Wednesday Dinner": 3, "Thursday Dinner": 4}

    d = dict(request.POST.iterlists())
    start_date = datetime.strptime(request.POST.get('start_date'), "%Y-%m-%d").date()

    Menu.objects.filter(start_date=start_date).delete()

    menu = Menu(start_date = start_date,
                servings = 24,
                notes = "none")
    menu.save()

    for key, item in d.items():
        if "day" in key:
            day_num = key.split("_")[1]
            meal_key = "item_" + day_num

            recipes = d[meal_key]
            meal = Meal(menu=menu,
                        date=start_date+timedelta(days_to_num[request.POST.get(key)]),
                        meal_name = request.POST.get(key))
            meal.save()

            for r in recipes:
                recipe = Recipe.objects.filter(recipe_name=r).first()
                meal.recipes.add(recipe)

    return HttpResponseRedirect(reverse('menu:index'))


class DetailView(generic.DetailView):
    model = Meal
    template_name = 'menu/display_meal.html'


def add_lateplate(request, pk):
    meal = get_object_or_404(Meal, pk=pk)

    l = LatePlate(name=request.POST.get("name"), meal=meal)
    l.save()

    return HttpResponseRedirect(reverse('menu:display_meal', args=[pk]))

def shopper(request, pk):
    template_name = 'menu/shopper.html'
    context_object_name = 'ingredient_dict'

    menu = get_object_or_404(Menu, pk=pk)

    all_ingredients = {}

    for meal in menu.meal_set.all():
        for recipe in meal.recipes.all():
            scale_factor = menu.servings/recipe.serving_size
            for ingredient in recipe.ingredient_set.all():
                if ingredient not in all_ingredients:
                    all_ingredients[ingredient] = ingredient.quantity * scale_factor
                else:
                    all_ingredients[ingredient] += ingredient.quantity * scale_factor

    return render(request, template_name, {context_object_name: all_ingredients})



