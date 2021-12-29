# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views import generic
from recipes.models import Recipe, Ingredient
from recipes.units.wrappers import RecipeWrapper

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.urls import reverse
from django.db.models.functions import Lower
from django.views.decorators.csrf import csrf_exempt

import logging
logger = logging.getLogger("recipes/views")

# Create your views here.

def detail(request, pk):
    template_name = 'recipes/detail.html'
    steward = False
    if request.user.is_authenticated and check_if_steward(request.user):
        steward = True

    recipe = get_object_or_404(Recipe, pk=pk)
    wrapped_recipe = RecipeWrapper(recipe)

    return render(request, template_name, {"recipe": wrapped_recipe,
                                           "steward": steward})

def view_recipes(request):
    recipes = Recipe.objects.all().order_by(Lower('recipe_name'))
    return render(request, "recipes/index.html", {"recipe_list": recipes})


class EditView(generic.DetailView):
    model = Recipe
    template_name = 'recipes/edit.html'


def add_recipe(request):
    return render(request, "recipes/add_recipe.html")


def submit_recipe(request):
    if request.user.is_authenticated:
        d = dict(request.POST.lists())
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
        d = dict(request.POST.lists())

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
    # To prevent accidentally deleting a recipe, for the request to be of type DELETE.
    if request.method != 'DELETE':
        return HttpResponseBadRequest('400 Bad Request: This method only allows DELETE requests.')

    # Check if user is authenticated properly
    if not request.user.is_authenticated:
        return HttpResponse('401 Unauthorized', status=401)
    if not check_if_steward(request.user):
        return HttpResponseForbidden('401 Unauthorized: User is not steward.', status=401)

    # Delete Recipe
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.delete()
    logger.info(f'Did delete recipe "{recipe}" with ID {recipe_id}.')

    return HttpResponse(status=200)


def check_if_steward(user):
    return user.groups.all().filter(name="stewards").count() > 0
