from django.apps import AppConfig
from django.db.models.signals import post_save


class BasicConfig(AppConfig):
    name = 'basic'

    def ready(self):
        from basic.signals import post_save_scout_hierarchy
        from basic.models import ScoutHierarchy
        post_save.connect(post_save_scout_hierarchy, sender=ScoutHierarchy,  dispatch_uid="post_save_scout_hierarchy")
