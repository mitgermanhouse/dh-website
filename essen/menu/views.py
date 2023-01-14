import collections
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import BadRequest
from django.db import transaction
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, TemplateView, View
from home.models import Member
from pytz import timezone
from recipes.models import Recipe

from essen.converters import DateConverter
from menu.forms import MealRatingForm
from menu.helper import combine_ingredients
from menu.models import Meal, MealDayTime, MealRating, MealTime, Menu, Weekday

# Create your views here.


class IndexView(TemplateView):
    template_name = "menu/index.html"
    context_object_name = "menu"

    def today(self):
        return datetime.now(timezone("EST")).date()

    def get_current_week_date(self):
        today = self.today()
        days_from_sunday = (today.weekday() + 1) % 7

        return today - timedelta(days=days_from_sunday)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get Menu for Date
        target_date = kwargs.get("date") or self.get_current_week_date()
        menu = Menu.objects.filter(start_date=target_date).first()

        # Today
        today = self.today()
        sorted_meals = []

        if menu is not None:
            for meal in (
                menu.meal_set.prefetch_related("recipes")
                .prefetch_related("meal_day_time")
                .order_by(*Meal.meal_order)
            ):
                sorted_meals.append({"meal": meal, "today": meal.date == today})

        context["menu"] = menu
        context["sorted_meals"] = sorted_meals
        context["page_date"] = target_date

        return context


class MenuEditView(PermissionRequiredMixin, DetailView):
    template_name = "menu/edit_menu.html"
    model = Menu
    context_object_name = "menu"
    meal_form_prefix = "meal"

    permission_required = "menu.change_menu"

    def recipe_to_dict(self, r):
        d = {
            "id": r.id,
            "text": r.name,
        }

        if r.category is not None:
            d["category"] = {
                "name": r.category.name,
                "color": r.category.color,
                "color_is_light": r.category.color_is_light,
            }

        return d

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu = self.object  # Can be None

        # Modify context
        context["sorted_meals"] = (
            menu.meal_set.prefetch_related("recipes")
            .prefetch_related("meal_day_time")
            .order_by(*Meal.meal_order)
            if menu is not None
            else None
        )

        recipes = (
            Recipe.objects.all()
            .select_related("category")
            .only("name", "id", "category__name", "category__color")
            .order_by(Lower("name"))
        )
        context["available_recipes_dict"] = {
            "data": [self.recipe_to_dict(r) for r in recipes]
        }

        context["weekdays"] = [(tag.value, tag.description) for tag in Weekday]
        context["meal_times"] = [(tag.value, tag.description) for tag in MealTime]

        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        meal_post = dict(request.POST.lists())

        # Delete old menu meals
        menu = self.get_object() or Menu()
        if menu is not None:
            # TODO: Currently we delete all manual lateplates when editing a menu.
            #       Maybe try to keep them...
            menu.meal_set.all().delete()

        # Check if menu already exists in the specified week
        start_date = DateConverter().to_python(request.POST.get("start_date"))
        if Menu.objects.filter(start_date=start_date).exclude(pk=menu.pk).count() > 0:
            raise ValueError("A menu already exists for this week.")

        # Validate Data
        meal_weekday = meal_post.get("meal-weekday")
        meal_time = meal_post.get("meal-time")
        meal_recipe_id = meal_post.get("meal-recipe")
        meal_recipe_count = [int(s) for s in meal_post.get("meal-recipe-count") or []]

        if not len(meal_weekday) == len(meal_time) == len(meal_recipe_count):
            raise ValueError("Inconsistent number of meals.")

        if len(meal_recipe_id) != sum(meal_recipe_count):
            raise ValueError("Inconsistent number of recipes.")

        if len(set(zip(meal_weekday, meal_time))) != len(meal_weekday):
            raise ValueError("The days and times of each meal should be unique.")

        # Get Recipes for Meals
        recipes_qs = Recipe.objects.filter(id__in=meal_recipe_id)
        meal_recipes = [recipes_qs.filter(id=r_id).first() for r_id in meal_recipe_id]

        if None in meal_recipes:
            raise ValueError("Invalid recipe selected.")

        meal_recipes_grouped = []
        meal_recipes_group_offset = 0
        for count in meal_recipe_count:
            meal_recipes_grouped.append(
                meal_recipes[
                    meal_recipes_group_offset : meal_recipes_group_offset + count
                ]
            )
            meal_recipes_group_offset += count

        # Construct Menu
        menu.start_date = start_date
        menu.servings = int(request.POST.get("servings"))
        menu.notes = request.POST.get("notes")
        menu.save()

        # Construct Meals
        for i in range(len(meal_weekday)):
            meal_time[i]

            meal = Meal(
                menu=menu,
                date=start_date + timedelta(days=int(meal_weekday[i])),
                meal_day_time=MealDayTime.objects.filter(
                    weekday=int(meal_weekday[i]), meal_time=meal_time[i]
                ).first(),
            )

            meal.save()
            meal.recipes.set(meal_recipes_grouped[i])

        # raise ValueError('Not implemented... PLZ DONT COMMIT TO DATABASE :)')
        return HttpResponseRedirect(
            reverse("menu:index", args=[request.POST.get("start_date")])
        )


class MenuAddView(MenuEditView):
    permission_required = "menu.add_menu"

    def get_object(self):
        return None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["start_date"] = self.kwargs.get("date")
        return context


class MenuDeleteView(PermissionRequiredMixin, DetailView):
    permission_required = "menu.delete_menu"
    model = Menu
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()

        return HttpResponseRedirect(reverse("menu:index"))


class ModifyLateplate(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        meal = get_object_or_404(Meal, pk=kwargs.get("pk"))
        member = get_object_or_404(Member, pk=request.POST.get("name"))

        response = HttpResponseRedirect(
            reverse("menu:display_meal", args=[kwargs.get("pk")])
        )

        if "action_add" in request.POST:
            meal.manual_lateplates.add(member)
            meal.save()
            return response

        if "action_remove" in request.POST:
            meal.manual_lateplates.remove(member)
            meal.deleted_auto_lateplates.add(member)
            meal.save()

            return response

        raise BadRequest("Invalid form action.")


class MealView(DetailView):
    template_name = "menu/display_meal.html"
    model = Meal
    context_object_name = "meal"

    def get_queryset(self):
        return (
            Meal.objects.prefetch_related("recipes")
            .prefetch_related("recipes__ingredient_set")
            .prefetch_related("meal_day_time")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        scaled_recipes = [recipe for recipe in self.object.recipes.all()]
        [recipe.scale_to(self.object.menu.servings) for recipe in scaled_recipes]
        context["scaled_recipes"] = scaled_recipes
        context["members"] = (
            Member.objects.filter(user__is_active=True)
            .select_related("user")
            .order_by("user__first_name")
        )

        return context


class RateMealView(LoginRequiredMixin, DetailView):
    template_name = "menu/rate_meal.html"
    model = Meal

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        meal = self.get_object()

        # Get previous rating.
        # If it exists, update values using form, else create a new rating
        rating = meal.mealrating_set.filter(user=request.user).first() or MealRating()
        rating.user = request.user
        rating.meal = meal

        rating_form = MealRatingForm(instance=rating, data=request.POST)
        rating_form.save()

        return HttpResponseRedirect(reverse("menu:index"))


class ShopperView(DetailView):
    template_name = "menu/shopper.html"
    model = Menu
    context_object_name = "menu"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        menu = self.object
        meal_set = (
            menu.meal_set.order_by(*Meal.meal_order)
            .prefetch_related("recipes")
            .prefetch_related("recipes__ingredient_set")
            .select_related("meal_day_time")
        )
        meals_id = [meal.id for meal in meal_set]

        # Filter out all meals before the after_meal
        after_meal_pk = self.request.GET.get("after_meal")
        after_meal = menu.meal_set.filter(pk=after_meal_pk).first()

        if after_meal is not None and after_meal.id in meals_id:
            context["after_meal"] = after_meal
            offset = meals_id.index(after_meal.id) + 1

            meal_set = meal_set[offset:]

        context["ingredients"] = combine_ingredients(meal_set)

        return context


class ReviewsView(PermissionRequiredMixin, TemplateView):
    template_name = "menu/menu_reviews.html"
    permission_required = "menu.view_mealrating"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ratings = (
            MealRating.objects.all()
            .select_related("user")
            .select_related("meal")
            .select_related("meal__meal_day_time")
            .prefetch_related("meal__recipes")
        )

        grouped_ratings = collections.defaultdict(list)
        for rating in ratings:
            grouped_ratings[rating.meal].append(rating)

        ratings_context = []
        for meal, meal_ratings in grouped_ratings.items():
            overall_rating = sum([r.rating for r in meal_ratings]) / len(meal_ratings)

            ratings_context.append(
                {
                    "meal": meal,
                    "overall_rating": overall_rating,
                    "comments": meal_ratings,
                }
            )

        ratings_context.sort(key=lambda e: e["meal"].date, reverse=True)
        context["ratings"] = ratings_context

        return context
