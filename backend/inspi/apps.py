from django.apps import AppConfig
from django.db.models.signals import post_save


class InspiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inspi'

    def ready(self):
        from inspi.signals import post_save_like
        from inspi.models import Like
        post_save.connect(post_save_like, sender=Like, dispatch_uid="post_save_Like")
