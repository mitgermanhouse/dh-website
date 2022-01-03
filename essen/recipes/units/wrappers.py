from recipes.units import units
from recipes.models import Recipe, Ingredient
import json

class RecipeWrapper:
	def __init__(self, recipe: Recipe, meal = None):
		self._recipe = recipe
		self.meal = meal

		self.id = self._recipe.id
		self.name = self._recipe.recipe_name
		self.directions = self._recipe.directions
		self.serving_size = self._recipe.serving_size

		self.ingredients = [
			IngredientWrapper(ingredient, self) 
			for ingredient in self._recipe.ingredient_set.all()
		]

		if self.meal is not None:
			self.scale_to(self.meal.menu.servings)

	def scale_to(self, servings: int):
		scalar = servings / self.serving_size
		for ingredient in self.ingredients:
			ingredient.scale(scalar)
		self.serving_size = servings


class IngredientWrapper:
	def __init__(self, ingredient: Ingredient, recipe: RecipeWrapper):
		self._ingredient = ingredient
		self.recipe = recipe

		self.id = self._ingredient.id
		self.name = self._ingredient.ingredient_name
		self.unit = units.dh_unit_parser(self._ingredient.units)
		self.quantity = units.ureg.Quantity(self._ingredient.quantity, self.unit)

		self._update()

	def __repr__(self):
		return f"({self.name}, {self.quantity_str} {self.unit_str})"

	def scale(self, mul: float):
		self.quantity *= mul
		self._update()

	def _update(self):
		self.simplified_q = units.simplify(self.quantity, units.units)

	@property
	def quantity_str(self):
		return self.magnitude_str + " " + self.unit_str

	@property
	def magnitude_str(self):
		return f"{round(self.simplified_q.m, 2):.3g}"

	@property
	def unit_str(self):
		if self.quantity.u == units.dimensionless:
			return self._ingredient.units

		return f"{self.simplified_q.u:~}"

	@property
	def original_unit_str(self):
		if self.quantity.u == units.dimensionless:
			return self._ingredient.units

		return f"{self.quantity.u:~}"


class RecipeJSONEncoder(json.JSONEncoder):
	def default(self, it):
		if isinstance(it, RecipeWrapper):
			return {
				"id": it.id,
				"name": it.name,
				"directions": it.directions,
				"serving_size": it.serving_size,
				"ingredients": it.ingredients
			}

		if isinstance(it, IngredientWrapper):
			return {
				"id": it.id,
				"name": it.name,
				"unit": it.quantity.unit_str,
				"quantity": it.quantity.m,
			}
		
		return json.JSONEncoder.default(self, it)
	