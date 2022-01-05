from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from django.db.models.functions import Lower

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import View, DetailView, ListView, TemplateView

from recipes.models import Recipe, Ingredient
from recipes.units.wrappers import RecipeWrapper
from recipes.forms import RecipeForm, IngredientForm

class RecipesListView(ListView):
    template_name = 'recipes/index.html'
    queryset = Recipe.objects.all().order_by(Lower('recipe_name'))
    context_object_name = 'recipe_list'

class RecipeDetailView(DetailView):
    template_name = 'recipes/detail.html'
    model = Recipe
    context_object_name = 'recipe'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return RecipeWrapper(obj)

class RecipeEditView(PermissionRequiredMixin, DetailView):
    template_name = 'recipes/edit_recipe.html'
    model = Recipe
    context_object_name = 'recipe'
    ingredients_form_prefix = 'ingredient'

    permission_required = 'recipes.change_recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.object # Can be None

        # Modify context
        context['recipe_form'] = RecipeForm(instance=recipe, label_suffix='')
        context['ingredient_form_empty'] = IngredientForm(
            label_suffix='', 
            prefix=RecipeEditView.ingredients_form_prefix, 
            initial={k:'' for k in IngredientForm.base_fields.keys()}
        )

        if recipe is not None:
            context['recipe'] = RecipeWrapper(recipe)
            context['ingredients_forms'] = [
                IngredientForm(instance=ingredient, label_suffix='', prefix=RecipeEditView.ingredients_form_prefix) 
                for ingredient in recipe.ingredient_set.all()
            ]
        else:
            context['ingredients_forms'] = [context['ingredient_form_empty']]

        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        recipe = self.get_object()

        # Save Recipe
        recipe_form = RecipeForm(instance=recipe, data=request.POST)
        recipe = recipe_form.save()

        # Delete old ingredients
        recipe.ingredient_set.all().delete()

        # Create new ingredients
        prefix_class = IngredientForm(prefix=RecipeEditView.ingredients_form_prefix)
        ingredient_field_keys = [prefix_class.add_prefix(key) for key in IngredientForm.base_fields.keys()]
        ingredient_fields = {key:request.POST.getlist(key) for key in ingredient_field_keys}

        num_ingredients = min([len(val) for _, val in ingredient_fields.items()])

        # Construct all ingredient forms
        for i in range(num_ingredients):
            data = {key:value[i] for key, value in ingredient_fields.items()}
            ingredient_form = IngredientForm(data=data, prefix=RecipeEditView.ingredients_form_prefix)
            ingredient = ingredient_form.save(commit=False)

            ingredient.recipe = recipe
            ingredient.save()

        return HttpResponseRedirect(reverse('recipes:detail', args=[recipe.pk]))

class RecipeAddView(RecipeEditView):
    permission_required = 'recipes.add_recipe'

    def get_object(self):
        return None

class RecipeDeleteView(PermissionRequiredMixin, DetailView):
    permission_required = 'recipes.delete_recipe'
    model = Recipe
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()

        return HttpResponseRedirect(reverse('recipes:index'))

