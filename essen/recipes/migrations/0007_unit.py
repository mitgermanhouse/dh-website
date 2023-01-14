# Generated by Django 3.2.11 on 2022-01-21 17:48

from django.db import migrations

from recipes.units import units


def parse_ingredient_unit(apps, schema_editor):
    live_layer_db = schema_editor.connection.alias
    Ingredient = apps.get_model("recipes", "Ingredient")

    # Wherever possible, replace unit string with proper unit symbol
    for ingredient in Ingredient.objects.using(live_layer_db).all():
        unit = units.dh_unit_parser(ingredient.unit)
        if unit != units.dimensionless:
            ingredient.unit = f"{unit:~}"
            ingredient.save()


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0006_auto_20220121_1744"),
    ]

    operations = [
        migrations.RunPython(parse_ingredient_unit, atomic=True),
    ]
