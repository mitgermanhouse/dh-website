from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = 'home'

    def ready(self):

        # Automatically delete tumbnails for images that get deleted

        from django_cleanup.signals import cleanup_pre_delete
        from easy_thumbnails.files import get_thumbnailer

        def easy_thumpnails_delete(**kwargs):
            image_field = kwargs['file']
            thumbnailer = get_thumbnailer(image_field)

            source_cache = thumbnailer.get_source_cache()
            thumbnailer.delete_thumbnails(source_cache)

            if source_cache:
                source_cache.delete()

        cleanup_pre_delete.connect(easy_thumpnails_delete)