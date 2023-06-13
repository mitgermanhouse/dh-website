import colorsys

import django.db.models
from colorfield.fields import ColorField
from django.db import models


class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()
    category = models.ForeignKey(
        "faqs.Category",
        on_delete=django.db.models.deletion.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.question


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
