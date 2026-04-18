from django.apps import AppConfig


class PetsConfig(AppConfig):
    name = "pets"

    def ready(self):
        pass
