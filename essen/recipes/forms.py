from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

from essen.widgets import Select2Widget
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
        fields = ('name', 'serving_size', 'directions', 'category')

        labels = {
            'name': 'Name',
            'serving_size': 'Serving Size',
            'directions': 'Directions',
            'category': 'Category'
        }

        widgets = {
            'category': Select2Widget(data_values=['color', 'color_is_light'])
        }


    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.fields['category'].empty_label = '- None -'

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'

        self.helper.layout = Layout(
            'name',
            'serving_size',
            'directions',
            Field('category', css_class='select2category')
        )

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