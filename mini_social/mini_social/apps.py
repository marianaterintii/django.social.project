from django.apps import AppConfig
from django.db.models.signals import post_save

class SignalEmailNotificationConfig(AppConfig):
    name = 'mini_social'
    def ready(self):
        from . import signals
        post_save.connect(signals.postPublishedCallback)