from django.apps import AppConfig


class WellpaperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wellpaper'


    def ready(self):
        from . import signals