from django.apps import AppConfig
from django.conf import settings


class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'

    def ready(self):
        if settings.AUTOMATIC_NEWS_UPDATE:
            from main_app.scheduler import v1 as scheduler
            scheduler.startAutomaticTasks()
