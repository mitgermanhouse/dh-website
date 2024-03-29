# Generated by Django 3.2.11 on 2022-01-22 18:52

import colorfield.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0007_unit"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Short descriptive name for this category.",
                        max_length=127,
                        unique=True,
                    ),
                ),
                (
                    "color",
                    colorfield.fields.ColorField(
                        default="#adadab",
                        help_text=(
                            "The color that should get used when displaying this"
                            " category."
                        ),
                        image_field=None,
                        max_length=18,
                        samples=None,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="recipe",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="recipes.category",
            ),
        ),
    ]
