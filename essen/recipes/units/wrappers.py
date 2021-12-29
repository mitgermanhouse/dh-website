from recipes.units import units
from recipes.models import Recipe, Ingredient

class RecipeWrapper:
	def __init__(self, recipe: Recipe):
		self._recipe = recipe

		self.id = self._recipe.id
		self.name = self._recipe.recipe_name
		self.directions = self._recipe.directions
		self.serving_size = self._recipe.serving_size

		self.ingredients = [
			IngredientWrapper(ingredient) 
			for ingredient in self._recipe.ingredient_set.all()
		]

	def scale_to(self, servings: int):
		scalar = servings / self.serving_size
		for ingredient in self.ingredients:
			ingredient.scale(scalar)
		self.serving_size = servings


class IngredientWrapper:
	def __init__(self, ingredient: Ingredient):
		self._ingredient = ingredient

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
	def unit_str(self):
		if self.quantity.u == units.dimensionless:
			return self._ingredient.units

		return f"{self.simplified_q.u:~}"

	@property
	def quantity_str(self):
		return f"{round(self.simplified_q.m, 2):g}"

	