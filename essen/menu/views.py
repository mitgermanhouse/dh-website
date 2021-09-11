# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views import generic
from datetime import datetime, timedelta
import sys
from recipes.models import Recipe, Ingredient
from menu.models import Menu, Meal, LatePlate, AutoLatePlate, MealRating
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime, timedelta
from pytz import timezone
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
    sorted_meals = []
    if menu != None:
        for meal in menu.meal_set.order_by('date').all():
            if meal.date == (datetime.utcnow() - timedelta(hours=4)).date():
                sorted_meals.append({"today": True, "meal": meal})
            else:
                sorted_meals.append({"today": False, "meal": meal})
    print(sorted_meals)
    return render(request, template_name, {context_object_name: menu, 'target_date': target_date,
                                           'sorted_meals' : sorted_meals})

def add_menu(request):
    template_name = "menu/add_menu.html"
    context_object_name = 'recipe_choices'

    recipe_choices = Recipe.objects.all()

    return render(request, template_name, {context_object_name: recipe_choices, 'steward': check_if_steward(request.user)})


def getLatePlateText(user):
    '''
    Gets the text to be displayed for a specific user's lateplate based on their
    dietary restrictions and full name
    :return: string w/ html codes
    '''
    auto_plate = AutoLatePlate.objects.filter(username=user.username).first()
    dietary = ""
    emoji_mapping = {"Vegetarian": "&#x1F33F", "Lactose Free": "&#x1f95b", "Nut Free": "&#x1F95C",
                     "No Pork": "&#x1F437", "No Red Meat": "&#x1f969", "No Seafood": "&#x1f41f",
                     "No Raw Apple": "&#x1F34E", "No Coconut": "&#x1F965", "No Raw Carrots": "&#x1F955", 
                     "Gluten Free": "&#x1F35E", "No Mushroom": "&#x1F344"}
    if auto_plate != None and len(auto_plate.dietary) > 0:
        for restriction in auto_plate.dietary.split(";"):
            if dietary == "":
                dietary += " "
            dietary += emoji_mapping[restriction]

    return user.get_full_name() + dietary

def submit_menu(request):
    if not (request.user.is_authenticated and check_if_steward(request.user)):
        return HttpResponseRedirect(reverse('menu:index'))

    days_to_num = {"Sunday Brunch": 0, "Sunday Dinner": 0, "Monday Dinner": 1, "Tuesday Dinner": 2,
                   "Wednesday Dinner": 3, "Thursday Dinner": 4}

    d = dict(request.POST.iterlists())
    start_date = datetime.strptime(request.POST.get('start_date'), "%Y-%m-%d").date()

    Menu.objects.filter(start_date=start_date).delete()

    menu = Menu(start_date = start_date,
                servings = request.POST.get("serving_size"),
                notes = request.POST.get("notes"))
    menu.save()


    for key, item in d.items():
        if "day" in key:
            day_num = key.split("_")[1]
            meal_key = "item_" + day_num

            recipes = d[meal_key] #list of all recipe names corresponding to that meal in the menu
            meal = Meal(menu=menu,
                        date=start_date+timedelta(days_to_num[request.POST.get(key)]),
                        meal_name=request.POST.get(key))
            meal.save()

            # add automatic lateplates
            for auto_plate in AutoLatePlate.objects.all():
                if str(request.POST.get(key)) in str(auto_plate.days):
                    user = User.objects.filter(username=auto_plate.username).first()
                    l = LatePlate(meal=meal,
                                  name=getLatePlateText(user))
                    l.save()

            # add recipes
            for r in recipes:
                recipe = Recipe.objects.filter(recipe_name=r).first()
                meal.recipes.add(recipe)

    return HttpResponseRedirect(reverse('menu:index'))

class DetailView(generic.DetailView):
    model = Meal
    template_name = "menu/rate_meal.html"

def view_meal(request, pk):
    template_name = 'menu/display_meal.html'
    context_object_name = 'info'

    meal = get_object_or_404(Meal, pk=pk)
    info = {"meal" : meal, "users" : User.objects.exclude(username="admin").order_by('first_name')}

    return render(request, template_name, {context_object_name: info})


def add_lateplate(request, meal_pk, user_pk):
    meal = get_object_or_404(Meal, pk=meal_pk)

    username = request.POST.get("name")
    print(request.POST)
    print(username)
    user = User.objects.filter(username=username).first()

    if user.is_authenticated:
        l = LatePlate(name=getLatePlateText(user), meal=meal)
        l.save()

    return HttpResponseRedirect(reverse('menu:display_meal', args=[meal_pk]))

def remove_lateplate(request, lateplate_pk, user_pk):
    lateplate = get_object_or_404(LatePlate, pk=lateplate_pk)

    if request.user.is_authenticated:
        meal_id = lateplate.meal.id
        lateplate.delete()

    return HttpResponseRedirect(reverse('menu:display_meal', args=[meal_id]))


def auto_lateplates(request):
    template_name = 'menu/auto_lateplates.html'
    map = {"Sunday Brunch": 0, "Sunday Dinner": 1, "Monday Dinner": 2, "Tuesday Dinner": 3,
                   "Wednesday Dinner": 4, "Thursday Dinner": 5}
    requested_days = [{"day": "Sunday Brunch", "state": False}, {"day": "Sunday Dinner", "state": False}, {"day": "Monday Dinner", "state": False},
                      {"day": "Tuesday Dinner", "state": False},  {"day": "Wednesday Dinner", "state": False}, {"day": "Thursday Dinner", "state": False},]

    dietary_map = {"Vegetarian": 0, "Lactose Free": 1, "Nut Free": 2, "No Pork": 3, "No Red Meat": 4, "No Seafood": 5,
                   "No Raw Apple": 6, "No Coconut": 7, "No Raw Carrots": 8, "Gluten Free": 9, "No Mushroom": 9}
    restrictions = [{"restriction" : "Vegetarian", "state" : False}, {"restriction" : "Lactose Free", "state" : False},
                    {"restriction": "Nut Free", "state": False}, {"restriction": "No Pork", "state": False},
                    {"restriction": "No Red Meat", "state": False}, {"restriction": "No Seafood", "state": False},
                    {"restriction": "No Raw Apple", "state": False}, {"restriction": "No Coconut", "state": False}, 
                    {"restriction": "No Raw Carrots", "state": False}, {"restriction": "Gluten Free", "state": False}, 
                    {"restriction": "No Mushroom", "state": False}]

    lateplate = AutoLatePlate.objects.filter(username=request.user.username).first()

    if lateplate != None:
        if len(lateplate.days) > 0:
            for day in lateplate.days.split(";"):
                print("this is a day", day)
                requested_days[map[day]] = {"day": day, "state": True}

        if len(lateplate.dietary) > 0:
            for restriction in lateplate.dietary.split(";"):
                restrictions[dietary_map[restriction]] = {"restriction": restriction, "state": True}

    return render(request, template_name, {"days" : requested_days, "d_restrictions": restrictions})

def submit_auto_lateplates(request):
    if request.user.is_authenticated:
        d = dict(request.POST.iterlists())
        print(d)
        # delete the previous lateplate registrys
        AutoLatePlate.objects.filter(username=request.user.username).delete()
        # add the new one
        days = ""
        dietary = ""
        if "date" in d.keys():
            for day in d.get("date"):
                if days != "":
                    days += ";"
                days += day
                print(day)

        if "dietary" in d.keys():
            for restriction in d.get("dietary"):
                if dietary != "":
                    dietary += ";"
                dietary += restriction
        auto = AutoLatePlate(username=request.user.username, days=days, dietary=dietary)
        auto.save()

    return HttpResponseRedirect(reverse('menu:index'))


def shopper(request, pk):
    template_name = 'menu/shopper.html'
    context_object_name = 'ingredients'
    map = {"Sunday Brunch": 0, "Sunday Dinner": 1, "Monday Dinner": 2, "Tuesday Dinner": 3,
                   "Wednesday Dinner": 4, "Thursday Dinner": 5}

    menu = get_object_or_404(Menu, pk=pk)
    d = dict(request.GET.iterlists())

    after_filter = False
    after_date = (datetime.now() - timedelta(days=8)).date()
    if "filter_date" in d:
        after_date = map[d["after"][0]]
        after_filter = d["filter_date"][0]
    else:
        after_date = -1 # accept all recipes for shopping list

    all_ingredients = {}

    for meal in menu.meal_set.all():
        if map[meal.meal_name] > after_date:
            for recipe in meal.recipes.all():
                scale_factor = float(menu.servings)/recipe.serving_size
                for ingredient in recipe.ingredient_set.all():
                    ing_type = (ingredient.ingredient_name.lower(), ingredient.units.lower())
                    if ing_type not in all_ingredients:
                        all_ingredients[ing_type] = float(ingredient.quantity) * scale_factor
                    else:
                        all_ingredients[ing_type] += float(ingredient.quantity) * scale_factor

    ing_list = [{"ing": key[0], "quantity": value, "unit": key[1]} for key, value in all_ingredients.items()]
    ing_list.sort(key=lambda x: x["ing"])

    context_dict = {context_object_name: ing_list, "notes":menu.notes}
    if after_filter:
        context_dict["filter_date"] = after_filter
        context_dict["after"] = d["after"][0]
    return render(request, template_name, context_dict)


def ingredient_info(request, ing, menu):
    template_name = 'menu/ingredient_info.html'
    context_object_name = 'usages'

    search = get_object_or_404(Ingredient, pk=str(ing))
    menu = get_object_or_404(Menu, pk=str(menu))

    ingredient_uses = []

    for meal in menu.meal_set.all():
        for recipe in meal.recipes.all():
            scale_factor = menu.servings/recipe.serving_size
            for ingredient in recipe.ingredient_set.all():

                if ingredient.ingredient_name == search.ingredient_name and meal.date > datetime.now().date():
                    ingredient_uses.append(str(ingredient.quantity * scale_factor) + " " + ingredient.units + " for " + meal.meal_name)

    return render(request, template_name, {context_object_name: ingredient_uses})


def submit_rating(request, pk):
    if request.user.is_authenticated:
        d = dict(request.GET.iterlists())
        meal = get_object_or_404(Meal, pk=pk)

        print("rating", d)
        # rating = d[]

        if 'rate' in d:
            previous_rating = MealRating.objects.filter(username=request.user.username).filter(meal=meal)
            previous_rating.delete()

            rating = MealRating(meal=meal, username=request.user.username, rating=d['rate'][0], comment=d['comment-box'][0])
            rating.save()

        # MealRating(meal=meal, username=request.user.username, rating=)

    return HttpResponseRedirect(reverse('menu:index'))


def see_reviews(request):
    final_list = []
    steward = False
    if request.user.is_authenticated and check_if_steward(request.user):
        steward = True
        d = {}
        for review in MealRating.objects.all():
            if review.meal in d:
                d[review.meal].append((review.rating, review.comment, review.username))
            else:
                d[review.meal] = [(review.rating, review.comment, review.username)]

        print(d)

        final_list = []
        for key, item in d.items():
            overall_rating = float(sum([x[0] for x in item]))/len(item)
            comment_list = []
            for entry in item:
                comment_list.append({"username":entry[2], "comment":entry[1], "rating":entry[0]})
            final_list.append({"meal":key, "overall_rating":overall_rating, "comments":comment_list})
        final_list.sort(key=lambda entry: entry["meal"].date, reverse=True)

    return render(request, template_name="menu/menu_reviews.html", context={"all_meals": final_list, "steward":steward})

def check_if_steward(user):
    return user.groups.all().filter(name="stewards").count() > 0