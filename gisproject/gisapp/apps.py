from django.apps import AppConfig


class GisappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gisapp'

    def ready(self):
        import gisapp.signals