from django.apps import AppConfig


class ChCoworkingConfig(AppConfig):
    name = 'ch_coworking'
    verbose_name = "Coworking"

    def ready(self):
        from . import signals
