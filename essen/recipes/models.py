import colorsys

import django.db.models
from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.html import escape
from django.utils.safestring import SafeString

from essen.helper import reify, replace_url_with_link
from recipes.units import units


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    directions = models.TextField()
    serving_size = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)]
    )
    category = models.ForeignKey(
        "recipes.Category",
        on_delete=django.db.models.deletion.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    # -- Pint --
    _ingredient_scalar = 1
    _modified_serving_size = None

    def scale_to(self, servings: int):
        self._ingredient_scalar = servings / self.serving_size
        self._modified_serving_size = servings

    @property
    def actual_serving_size(self):
        if self._modified_serving_size is not None:
            return self._modified_serving_size
        else:
            return self.serving_size

    @property
    def directions_parts(self):
        d = self.directions.strip()
        d = escape(d)
        d = d.replace("\r\n", "\n").replace("\r", "\n")

        parts_delimiter = "\n\n" if "\n\n" in d else "\n"
        parts = d.split(parts_delimiter)
        parts = [p.strip().replace("\n", "<br>") for p in parts]
        parts = [p for p in parts if p]
        parts = [SafeString(replace_url_with_link(p)) for p in parts]

        return parts


class Ingredient(models.Model):
    name = models.CharField(max_length=255, null=True)
    unit = models.CharField(max_length=127, null=True)
    quantity = models.FloatField(default=0, validators=[MinValueValidator(0)])
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    # -- Pint --
    @reify
    def _p_unit(self):
        return units.dh_unit_parser(self.unit)

    @reify
    def _p_quantity(self):
        return (
            units.ureg.Quantity(self.quantity, self._p_unit)
            * self.recipe._ingredient_scalar
        )

    @reify
    def _p_simplified_quantity(self):
        return units.simplify(self._p_quantity, units.units)

    # -- Formatting --
    @reify
    def unit_str(self):
        if self._p_unit == units.dimensionless:
            return self.unit  # Return original unit string

        return f"{self._p_simplified_quantity.u:~}"

    @reify
    def magnitude_str(self):
        m = self._p_simplified_quantity.m
        if m >= 100:
            return str(int(m))
        return f"{round(m, 2):.3g}"


class Category(models.Model):
    name = models.CharField(
        max_length=127,
        unique=True,
        help_text="Short descriptive name for this category.",
    )
    color = ColorField(
        default="#adadab",
        help_text="The color that should get used when displaying this category.",
    )

    def __str__(self):
        return self.name

    @property
    def color_is_light(self):
        hex_code = self.color[1:]
        r, g, b = tuple(int(hex_code[i : i + 2], 16) / 255 for i in (0, 2, 4))
        h, l, s = colorsys.rgb_to_hls(r, g, b)  # noqa: E741

        return l >= 0.5
