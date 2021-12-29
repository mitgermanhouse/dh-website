from dataclasses import dataclass, field
from pint.quantity import Quantity

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

		self.meals = [
			MealWrapper(meal)
			for meal in self._menu.meal_set.all()
		]

class MealWrapper:
	def __init__(self, meal: Meal):
		self._meal = meal

		self.id = self._meal.id
		self.menu = self._meal.menu
		self.date = self._meal.date
		self.name = self._meal.meal_name
		self.lateplates = self._meal.lateplate_set.all()

		self.recipes = [
			RecipeWrapper(recipe)
			for recipe in self._meal.recipes.all()
		]

		# Properly scale recipe
		for recipe in self.recipes:
			recipe.scale_to(self.menu.servings)

@dataclass
class CombinedIngredients:
	name: str
	ingredients: list[IngredientWrapper] = field(default_factory=list)

	def __post_init__(self):
		self._quantities = None

	def matches(self, ingredient: IngredientWrapper):
		if self.name.lower() == ingredient.name.lower():
			return True

	def add(self, ingredient: IngredientWrapper):
		self.ingredients.append(ingredient)
		self.invalidate_quantities()

	def invalidate_quantities(self):
		'''Invalidates the computed quantities property.'''
		self._quantities = None

	@property
	def quantities(self) -> list[Quantity]:
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
			f"{round(q.m, 2):g} {q.u:~}" for q in self.quantities
		])

def combine_ingredients(meals: list[MealWrapper]) -> list[IngredientWrapper]:
	all_ingredients = {}

	for meal in meals:
		for recipe in meal.recipes:
			for ingredient in recipe.ingredients:
				ingredient_key = ingredient.name.lower()

				if ingredient_key in all_ingredients:
					all_ingredients[ingredient_key].add(ingredient)
				else:
					all_ingredients[ingredient_key] = CombinedIngredients(ingredient.name, [ingredient])

	combined_ingredients = list(all_ingredients.values())
	combined_ingredients.sort(key = lambda i: i.name.lower())

	return combined_ingredients

