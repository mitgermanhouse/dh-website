from django import forms
from recipes.models import Recipe, Ingredient
from recipes.units import units

class PintUnitInput(forms.TextInput):
    '''
    Custom form widget that transforms an arbitrary unit string to a
    normalized pint unit string.
    '''

    def format_value(self, value):
        unit = units.dh_unit_parser(value)

        if unit is None or unit == units.dimensionless:
            return value

        return f"{unit:~}"

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'directions', 'serving_size')

        labels = {
            'name': 'Name',
            'directions': 'Directions',
            'serving_size': 'Serving Size'
        }

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name', 'unit', 'quantity')

        labels = {
            'name': 'Ingredient',
            'unit': 'Unit',
            'quantity': 'Quantity'
        }

        widgets = {
            'unit': PintUnitInput()
        }