from django.contrib import admin

from recipes.models import Category, Ingredient, Recipe


class IngredientInline(admin.TabularInline):
    model = Ingredient
    fields = ("name", "quantity", "unit")


class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]
    search_fields = ["name", "id"]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category)
