# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views import generic
from recipes.models import Recipe, Ingredient
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def detail(request, pk):
    template_name = 'recipes/detail.html'
    steward = False
    if request.user.is_authenticated and check_if_steward(request.user):
        steward = True

    return render(request, template_name, {"recipe": get_object_or_404(Recipe, pk=pk),
                                                  "steward": steward})

def view_recipes(request):
    d = dict(request.GET.iterlists())
    print(d)
    search_key = d.get("searchbar", [""])[0]
    query_key = d.get("query", ["recipe_search"])[0]

    if 'searchbar' in d:
        if query_key == 'recipe_search':
            recipes = Recipe.objects.all().filter(recipe_name__icontains=search_key)
        elif search_key == "":
            recipes = Recipe.objects.all()
        else:
            recipes = []
            for recipe in Recipe.objects.all():
                for ing in recipe.ingredient_set.all():
                    if ing.ingredient_name.lower().find(search_key.lower()) > -1:
                        recipes.append(recipe)
                        break
    else:
        recipes = Recipe.objects.all()

    return render(request, "recipes/index.html", {"recipe_list": recipes, "searchbar": search_key, "query":query_key})



class EditView(generic.DetailView):
    model = Recipe
    template_name = 'recipes/edit.html'


def add_recipe(request):
    return render(request, "recipes/add_recipe.html")


def submit_recipe(request):
    if request.user.is_authenticated:
        d = dict(request.POST.iterlists())
        r = Recipe(recipe_name=d['recipe_name'][0], directions=d['directions'][0], serving_size=int(d['serving_size'][0]))
        r.save()
        print(d)
        if 'ingredient' in d:
            for i in range(len(d['ingredient'])):
                Ingredient(recipe=r, ingredient_name=d['ingredient'][i], units=d['units'][i],
                               quantity=float(d['quantity'][i])).save()

    return HttpResponseRedirect(reverse('recipes:detail', args=[r.id]))


def submit_edit(request, recipe_id):
    if request.user.is_authenticated and check_if_steward(request.user):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        for ingredient in recipe.ingredient_set.all():
            ingredient.delete()
        d = dict(request.POST.iterlists())

        recipe.serving_size = d['serving_size'][0]
        recipe.recipe_name = d['recipe_name'][0]
        recipe.directions = d['directions'][0]
        recipe.save()

        if 'ingredient' in d:
            for i in range(len(d['ingredient'])):
                Ingredient(recipe=recipe, ingredient_name=d['ingredient'][i], units=d['units'][i],
                               quantity=float(d['quantity'][i])).save()

    return HttpResponseRedirect(reverse('recipes:detail', args=[recipe_id]))

def delete(request, recipe_id):
    if request.user.is_authenticated and check_if_steward(request.user):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.delete()

    return HttpResponseRedirect(reverse('recipes:index'))


def check_if_steward(user):
    return user.groups.all().filter(name="stewards").count() > 0