import collections

from django.views.generic import View, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.db.models.functions import Lower

from django.shortcuts import render, get_object_or_404
from django.views import generic
from datetime import datetime, timedelta
import sys
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from pytz import timezone

from essen.converters import DateConverter
from recipes.models import Recipe, Ingredient
from home.models import Member
from menu.models import MealDayTime, Menu, Meal, MealRating
from menu.units.wrappers import MenuWrapper, MealWrapper, combine_ingredients
from menu.forms import MealRatingForm

# Create your views here.

class IndexView(TemplateView):
    template_name = 'menu/index.html'
    context_object_name = 'menu'

    def today(self):
        return datetime.now(timezone('EST')).today().date()

    def get_current_week_date(self):
        today = self.today()
        days_from_sunday = (today.weekday() + 1) % 7

        return today - timedelta(days=days_from_sunday)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get Menu for Date
        target_date = kwargs.get('date') or self.get_current_week_date()
        menu = Menu.objects.filter(start_date__year=target_date.year,
                                   start_date__month=target_date.month,
                                   start_date__day=target_date.day).first()

        # Today
        today = self.today()
        sorted_meals = []

        if menu is not None:
            for meal in menu.meal_set.prefetch_related('recipes').prefetch_related('meal_day_time').order_by(*Meal.meal_order):
                sorted_meals.append({
                    'meal': meal,
                    'today': meal.date == today
                })

        context['menu'] = menu
        context['sorted_meals'] = sorted_meals
        context['page_date'] = target_date

        return context


class MenuEditView(PermissionRequiredMixin, DetailView):
    template_name = 'menu/edit_menu.html'
    model = Menu
    context_object_name = 'menu'
    meal_form_prefix = 'meal'

    permission_required = 'menu.change_menu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu = self.object  # Can be None

        # Modify context
        context['sorted_meals'] = menu.meal_set.order_by(*Meal.meal_order) if menu is not None else None
        context['available_recipes'] = Recipe.objects.all().order_by(Lower('recipe_name'))

        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        meal_post = dict(request.POST.lists())

        # Delete old menu meals
        menu = self.get_object() or Menu()
        if menu is not None:
            # TODO: Currently we delete all manual lateplates when editing a menu. Maybe try to keep them...
            menu.meal_set.all().delete()

        # Check if menu already exists in the specified week
        start_date = DateConverter().to_python(request.POST.get('start_date'))
        if Menu.objects.filter(start_date=start_date).exclude(pk=menu.pk).count() > 0:
            raise ValueError('A menu already exists for this week.')

        # Validate Data
        meal_weekday = meal_post.get('meal-weekday')
        meal_time = meal_post.get('meal-time')
        meal_recipe_id = meal_post.get('meal-recipe')
        meal_recipe_count = [int(s) for s in meal_post.get('meal-recipe-count') or []]

        if not len(meal_weekday) == len(meal_time) == len(meal_recipe_count):
            raise ValueError('Inconsistent number of meals.')

        if len(meal_recipe_id) != sum(meal_recipe_count):
            raise ValueError('Inconsistent number of recipes.')

        if len(set(zip(meal_weekday, meal_time))) != len(meal_weekday):
            raise ValueError('The days and times of each meal should be unique.')

        # Get Recipes for Meals
        recipes_qs = Recipe.objects.filter(id__in=meal_recipe_id)
        meal_recipes = [recipes_qs.filter(id=id).first() for id in meal_recipe_id]

        if None in meal_recipes:
            raise ValueError('Invalid recipe selected.')

        meal_recipes_grouped = []
        meal_recipes_group_offset = 0
        for count in meal_recipe_count:
            meal_recipes_grouped.append(meal_recipes[meal_recipes_group_offset : meal_recipes_group_offset+count])
            meal_recipes_group_offset += count

        # Construct Menu
        menu.start_date = start_date
        menu.servings = int(request.POST.get('servings'))
        menu.notes = request.POST.get('notes')
        menu.save()

        # Construct Meals
        for i in range(len(meal_weekday)):
            time = meal_time[i]

            meal = Meal(
                menu = menu,
                date = start_date + timedelta(days=int(meal_weekday[i])),
                meal_day_time = MealDayTime.objects.filter(weekday=int(meal_weekday[i]), meal_time=meal_time[i]).first()
            )

            meal.save()
            meal.recipes.set(meal_recipes_grouped[i])

        # raise ValueError('Not implemented... PLZ DONT COMMIT TO DATABASE :)')
        return HttpResponseRedirect(reverse('menu:index', args=[request.POST.get('start_date')]))


class MenuAddView(MenuEditView):
    permission_required = 'menu.add_menu'

    def get_object(self):
        return None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start_date'] = self.kwargs.get('date')
        return context


class MenuDeleteView(PermissionRequiredMixin, DetailView):
    permission_required = 'menu.delete_menu'
    model = Menu
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()

        return HttpResponseRedirect(reverse('menu:index'))


class ModifyLateplate(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        meal = get_object_or_404(Meal, pk=kwargs.get('pk'))
        member = get_object_or_404(Member, pk=request.POST.get('name'))

        response = HttpResponseRedirect(reverse('menu:display_meal', args=[kwargs.get('pk')]))

        if 'action_add' in request.POST:
            meal.manual_lateplates.add(member)
            meal.save()
            return response

        if 'action_remove' in request.POST:
            meal.manual_lateplates.remove(member)
            meal.deleted_auto_lateplates.add(member)
            meal.save()

            return response

        # TODO: Raise Instead
        return HttpResponseBadRequest()


class MealView(DetailView):
    template_name = 'menu/display_meal.html'
    model = Meal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['meal'] = MealWrapper(self.object)
        context['members'] = Member.objects.filter(user__is_active=True).select_related('user').order_by('user__first_name')

        return context


class RateMealView(LoginRequiredMixin, DetailView):
    template_name = 'menu/rate_meal.html'
    model = Meal

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        meal = self.get_object()

        # Get previous rating. If it exists, update values using form, else create a new rating
        rating = meal.mealrating_set.filter(username=request.user.username).first() or MealRating()
        rating.username = request.user.username
        rating.meal = meal

        rating_form = MealRatingForm(instance=rating, data=request.POST)
        rating_form.save()

        return HttpResponseRedirect(reverse('menu:index'))


class ShopperView(DetailView):
    template_name = 'menu/shopper.html'
    model = Menu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        menu = MenuWrapper(self.object)
        meals = menu.meals
        meals_id = [meal.id for meal in meals]

        # Filter out all meals before the after_meal
        after_meal_pk = self.request.GET.get('after_meal')
        after_meal = self.object.meal_set.filter(pk=after_meal_pk).first()

        if after_meal is not None and after_meal.id in meals_id:
            meals = meals[meals_id.index(after_meal.id)+1:]
            context['after_meal'] = MealWrapper(after_meal)

        context['menu'] = menu
        context['ingredients'] = combine_ingredients(meals)

        return context


class ReviewsView(PermissionRequiredMixin, TemplateView):
    template_name = 'menu/menu_reviews.html'
    permission_required = 'menu.view_meal_rating'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ratings = MealRating.objects.all().select_related('user').select_related('meal').select_related('meal__meal_day_time').prefetch_related('meal__recipes')

        grouped_ratings = collections.defaultdict(list)
        for rating in ratings:
            grouped_ratings[rating.meal].append(rating)

        ratings_context = []
        for meal, meal_ratings in grouped_ratings.items():
            overall_rating = sum([r.rating for r in meal_ratings]) / len(meal_ratings)

            ratings_context.append({
                'meal': meal,
                'overall_rating': overall_rating,
                'comments': meal_ratings
            })

        ratings_context.sort(key=lambda e: e['meal'].date, reverse=True)
        context['ratings'] = ratings_context

        return context
