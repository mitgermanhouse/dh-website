from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.cache import get_cache_key
from django.utils.feedgenerator import Atom1Feed

from faqs.models import Faq


class FaqsFeed(Feed):
    feed_type = Atom1Feed
    title = "German House Faqs"
    link = "/faqs/feed/"
    description = "All the faqs..."
    description_template = "faqs/feed/faq_description.html"

    Item = Faq

    def __call__(self, request, *args, **kwargs):
        cache_key = get_cache_key(request)
        if response := cache.get(cache_key):
            return response

        response = super().__call__(request, *args, **kwargs)
        cache.set(cache_key, response, 60 * 15)
        return response

    def items(self):
        return (
            Faq.objects.all()
            .order_by(Lower("question"))
        )

    def item_title(self, item: Item):
        return item.name

    def item_link(self, item: Item):
        return reverse("faqs:detail", args=[item.pk])

    def item_guid(self, item: Item):
        return item.pk
