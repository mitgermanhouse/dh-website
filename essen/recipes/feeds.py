from django.contrib.syndication.views import Feed
from django.db.models.functions import Lower
from django.urls import reverse

from recipes.models import Recipe


class RecipesFeed(Feed):
    title = "German House Recipes"
    link = "/recipes/feed/"
    description = "All the recipes..."

    def items(self):
        return Recipe.objects.all().only("name", "id").order_by(Lower("name"))

    def item_title(self, item):
        return item.name

    def item_link(self, item):
        return reverse("recipes:detail", args=[item.pk])
