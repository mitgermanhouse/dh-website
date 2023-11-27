import copy
import re
from dataclasses import dataclass, field
from typing import List

from pint.quantity import Quantity
from recipes.models import Ingredient
from recipes.units import units

from menu.models import Meal, MealTime


@dataclass
class CombinedIngredients:
    name: str
    ingredients: List[Ingredient] = field(default_factory=list)

    def __post_init__(self):
        self.invalidate()

    def add(self, ingredient: Ingredient):
        self.ingredients.append(ingredient)
        self.invalidate()

    def invalidate(self):
        """Invalidates all computed properties."""
        self._quantities = None

    @property
    def quantities(self) -> List[Quantity]:
        if self._quantities is not None:
            return self._quantities

        # Compute quantity list
        ans = {}

        for ingredient in self.ingredients:
            dimensionality = ingredient._p_unit.dimensionality
            if dimensionality in ans:
                ans[dimensionality] += ingredient._p_quantity
            else:
                ans[dimensionality] = ingredient._p_quantity

        self._quantities = [units.simplify(q, units.units) for q in ans.values()]
        return self._quantities

    @property
    def quantities_str(self):
        return ", ".join([f"{round(q, 2):.3g~}" for q in self.quantities])


__paren_regex = re.compile(r"\(.*\)")
__cache = []


def combine_ingredients(meals: List[Meal]) -> List[CombinedIngredients]:
    all_ingredients = {}

    def ingr_key(ingredient: Ingredient) -> str:
        key = ingredient.name.lower()
        key = re.sub(__paren_regex, "", key)
        key = key.split(",")[0]
        key = key.strip()

        return key

    for meal in meals:
        servings = meal.menu.servings
        for recipe in meal.recipes.all():
            if meal.meal_day_time.meal_time != MealTime.BIRTHDAYS.value:
                recipe.scale_to(servings)

            # Set associated_meal variable for future reference in the template
            recipe.associated_meal = meal

            for ingredient in recipe.ingredient_set.all():
                # INFO: If the same recipe gets used multiple times, the same recipe
                #       object gets reused multiple times. This is why in this case we
                #       must create a copy of the ingredient and change the
                #       associated recipe.
                if ingredient.recipe is not recipe:
                    ingredient = copy.copy(ingredient)
                    ingredient.recipe = recipe

                    # Prevent saving or deleting the copy.
                    # This probably isn't necessary...
                    def _raise(*args, **kwargs):
                        raise AttributeError("You are not allowed to modify a copy.")

                    ingredient.save = _raise
                    ingredient.delete = _raise

                ingredient_key = ingr_key(ingredient)
                if ingredient_key in all_ingredients:
                    all_ingredients[ingredient_key].add(ingredient)
                else:
                    all_ingredients[ingredient_key] = CombinedIngredients(
                        ingredient_key, [ingredient]
                    )

                # If the same recipe gets used multiple times BAD
                print(ingredient.recipe is recipe)

    combined_ingredients = list(all_ingredients.values())
    combined_ingredients.sort(key=lambda i: i.name.lower())

    return combined_ingredients
