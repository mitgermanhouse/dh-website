# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Recipe, Ingredient
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'recipes/index.html'
    model = Recipe


class DetailView(generic.DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'


class EditView(generic.DetailView):
    model = Recipe
    template_name = 'recipes/edit.html'


def add_recipe(request):
    return render(request, "recipes/add_recipe.html")


def submit_recipe(request):
    d = dict(request.POST.iterlists())
    r = Recipe(recipe_name=d['recipe_name'][0], directions=d['directions'][0], serving_size=int(d['serving_size'][0]))
    r.save()

    for i in range(len(d['ingredient'])):
        Ingredient(recipe=r, ingredient_name=d['ingredient'][i], units=d['units'][i],
                       quantity=float(d['quantity'][i])).save()

    return HttpResponseRedirect(reverse('recipes:detail', args=[r.id]))


def submit_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    for ingredient in recipe.ingredient_set.all():
        ingredient.delete()
    d = dict(request.POST.iterlists())

    for i in range(len(d['ingredient'])):
        Ingredient(recipe=recipe, ingredient_name=d['ingredient'][i], units=d['units'][i],
                       quantity=float(d['quantity'][i])).save()

    return HttpResponseRedirect(reverse('recipes:detail', args=[recipe_id]))

