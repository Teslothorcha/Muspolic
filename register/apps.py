from django.apps import AppConfig


class RegisterConfig(AppConfig):
    name = 'register'

    def ready(self):
        import register.signals
        