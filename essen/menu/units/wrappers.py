from dataclasses import dataclass, field
from typing import List, Optional
from pint.quantity import Quantity
import re

from essen.helper import reify
from recipes.units import units
from recipes.units.wrappers import RecipeWrapper, IngredientWrapper
from menu.models import Meal, Menu

class MenuWrapper:
	def __init__(self, menu: Menu):
		self._menu = menu

		self.id = self._menu.id
		self.start_date = self._menu.start_date
		self.servings = self._menu.servings
		self.notes = self._menu.notes

	@reify
	def meals(self):
		return [MealWrapper(meal, self) for meal in self._menu.meal_set.order_by(*Meal.meal_order)]


class MealWrapper:
	def __init__(self, meal: Meal, menu: Optional[MenuWrapper] = None):
		self._meal = meal
		
		if menu is not None:
			self.menu = menu
		else:
			self.menu = MenuWrapper(self._meal.menu)

		self.id = self._meal.id
		self.date = self._meal.date
		self.name = self._meal.name
		self.lateplates = self._meal.lateplates

	@reify
	def recipes(self):
		return [RecipeWrapper(recipe, self) for recipe in self._meal.recipes.all()]

@dataclass
class CombinedIngredients:
	name: str
	ingredients: List[IngredientWrapper] = field(default_factory=list)

	def __post_init__(self):
		self.invalidate()

	def add(self, ingredient: IngredientWrapper):
		self.ingredients.append(ingredient)
		self.invalidate()

	def invalidate(self):
		'''Invalidates all computed properties.'''
		self._quantities = None

	@property
	def quantities(self) -> List[Quantity]:
		if self._quantities is not None:
			return self._quantities

		# Compute quantity list
		ans = {}

		for ingredient in self.ingredients:
			if ingredient.unit.dimensionality in ans:
				ans[ingredient.unit.dimensionality] += ingredient.quantity
			else:
				ans[ingredient.unit.dimensionality] = ingredient.quantity

		self._quantities = [units.simplify(q, units.units) for q in ans.values()]
		return self._quantities

	@property
	def quantities_str(self):
		return ", ".join([
			f"{round(q, 2):.3g~}" for q in self.quantities
		])

__paren_regex = re.compile(r"\(.*\)")
def combine_ingredients(meals: List[MealWrapper]) -> List[CombinedIngredients]:
	all_ingredients = {}

	def ingr_key(ingredient: IngredientWrapper) -> str:
		key = ingredient.name.lower()
		key = re.sub(__paren_regex, '', key)
		key = key.split(',')[0]
		key = key.strip()

		return key

	for meal in meals:
		for recipe in meal.recipes:
			for ingredient in recipe.ingredients:
				ingredient_key = ingr_key(ingredient)

				if ingredient_key in all_ingredients:
					all_ingredients[ingredient_key].add(ingredient)
				else:
					all_ingredients[ingredient_key] = CombinedIngredients(ingredient_key, [ingredient])

	combined_ingredients = list(all_ingredients.values())
	combined_ingredients.sort(key = lambda i: i.name.lower())

	return combined_ingredients

