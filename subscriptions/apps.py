from django.apps.config import AppConfig


class MainApp(AppConfig):
    name = 'subscriptions'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from . import signal_handlers
