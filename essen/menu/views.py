import collections

from django.views.generic import TemplateView, DetailView
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
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime, timedelta
from pytz import timezone

from recipes.models import Recipe, Ingredient
from menu.models import Menu, Meal, MealRating
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
        date_str = kwargs.get('date')

        # Get Menu for Date
        target_date = self.get_current_week_date() if date_str is None else datetime.strptime(date_str, '%m/%d/%Y')
        menu = Menu.objects.filter(start_date__year=target_date.year,
                                   start_date__month=target_date.month,
                                   start_date__day=target_date.day).first()

        # Today
        today = self.today()
        sorted_meals = []

        if menu is not None:
            for meal in menu.meal_set.order_by('date').all():
                sorted_meals.append({
                    'meal': meal,
                    'today': meal.date == today
                })

        context['menu'] = menu
        context['sorted_meals'] = sorted_meals
        context['target_date'] = target_date

        return context


# TODO: Edit Menu View
#        -> Add Menu View


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
        context['sorted_meals'] = menu.meal_set.order_by('date').all() if menu is not None else None
        context['available_recipes'] = Recipe.objects.all().order_by(Lower('recipe_name'))

        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        meal_post = dict(request.POST.lists())

        # Delete old menu meals
        menu = self.get_object() or Menu()
        if menu is not None:
            menu.meal_set.all().delete()

        # Check if menu already exists in the specified week
        start_date = datetime.strptime(request.POST.get('start_date'), "%Y-%m-%d").date()
        if Menu.objects.filter(start_date=start_date).exclude(pk=menu.pk).count() > 0:
            raise ValueError('A menu already exists for this week.')

        # Validate Data
        meal_day = meal_post.get('meal-day')
        meal_time = meal_post.get('meal-time')
        meal_recipe_id = meal_post.get('meal-recipe')
        meal_recipe_count = [int(s) for s in meal_post.get('meal-recipe-count') or []]

        if not len(meal_day) == len(meal_time) == len(meal_recipe_count):
            raise ValueError('Inconsistent number of meals.')

        if len(meal_recipe_id) != sum(meal_recipe_count):
            raise ValueError('Inconsistent number of recipes.')

        if len(set(zip(meal_day, meal_time))) != len(meal_day):
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
        for i in range(len(meal_day)):
            time = meal_time[i]

            meal = Meal(
                menu = menu,
                date = start_date + timedelta(days=int(meal_day[i])),
                meal_name = "*** SOME MEAL NAME ***" # TODO: --->  Transition model so that this is not required anymore
            )

            meal.save()
            meal.recipes.set(meal_recipes_grouped[i])

        # TODO: Add Automatic Lateplates

        raise ValueError('Not implemented... PLZ DONT COMMIT TO DATABASE :)')
        return HttpResponseRedirect(reverse('menu:index'))


class MenuAddView(MenuEditView):
    permission_required = 'menu.add_menu'

    def get_object(self):
        return None


class MenuDeleteView(PermissionRequiredMixin, DetailView):
    permission_required = 'menu.delete_menu'
    model = Menu
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()

        return HttpResponseRedirect(reverse('menu:index'))


@login_required
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

@login_required
def submit_menu(request):
    if not (request.user.is_authenticated and check_if_steward(request.user)):
        return HttpResponseRedirect(reverse('menu:index'))

    days_to_num = {"Sunday Brunch": 0, "Sunday Dinner": 0, "Monday Dinner": 1, "Tuesday Dinner": 2,
                   "Wednesday Dinner": 3, "Thursday Dinner": 4}

    d = dict(request.POST.lists())
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


class MealView(DetailView):
    template_name = 'menu/display_meal.html'
    model = Meal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['meal'] = MealWrapper(self.object)
        context['users'] = User.objects.exclude(username='admin').order_by('first_name')

        return context


def modify_lateplate(request, meal_pk, user_pk):
    meal = get_object_or_404(Meal, pk=meal_pk)
    username = request.POST.get("name")
    user = User.objects.filter(username=username).first()

    response = HttpResponseRedirect(reverse('menu:display_meal', args=[meal_pk]))

    if user is None or not user.is_authenticated:
        return response

    if "action_add" in request.POST:
        l = LatePlate(name=getLatePlateText(user), meal=meal)
        l.save()
        return response

    if "action_remove" in request.POST:
        for lp in LatePlate.objects.filter(meal=meal, name__contains=user.get_full_name()):
            lp.delete()
        return response

    return HttpResponseBadRequest()


def auto_lateplates(request):
    template_name = 'menu/auto_lateplates.html'
    map = {"Sunday Brunch": 0, "Sunday Dinner": 1, "Monday Dinner": 2, "Tuesday Dinner": 3,
                   "Wednesday Dinner": 4, "Thursday Dinner": 5}
    requested_days = [{"day": "Sunday Brunch", "state": False}, {"day": "Sunday Dinner", "state": False}, {"day": "Monday Dinner", "state": False},
                      {"day": "Tuesday Dinner", "state": False},  {"day": "Wednesday Dinner", "state": False}, {"day": "Thursday Dinner", "state": False},]

    dietary_map = {"Vegetarian": 0, "Lactose Free": 1, "Nut Free": 2, "No Pork": 3, "No Red Meat": 4, "No Seafood": 5,
                   "No Raw Apple": 6, "No Coconut": 7, "No Raw Carrots": 8, "Gluten Free": 9, "No Mushroom": 10}
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
        d = dict(request.POST.lists())
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


class ShopperView(DetailView):
    template_name = 'menu/shopper.html'
    model = Menu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        menu = MenuWrapper(self.object)
        meals = menu.meals

        # TODO: Fix problem
        #        - Sunday Brunch and Sunday Dinner have the same date.
        #        - This means that I can't filter them based on the date.
        #        - To fix this, I have to make some modifications to the Meal model

        # Filter out all meals before the 
        after_meal_pk = self.request.GET.get('after_meal')
        if after_meal_pk is not None:
            after_meal = self.object.meal_set.filter(pk=after_meal_pk).first()
            meals = [m for m in meals if m.date > after_meal.date]
            context['after_meal'] = MealWrapper(after_meal)

        context['menu'] = menu
        context['ingredients'] = combine_ingredients(meals)

        return context


class ReviewsView(PermissionRequiredMixin, TemplateView):
    template_name = 'menu/menu_reviews.html'
    permission_required = 'menu.view_meal_rating'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ratings = MealRating.objects.all()

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


def check_if_steward(user):
    return user.groups.all().filter(name="stewards").count() > 0
