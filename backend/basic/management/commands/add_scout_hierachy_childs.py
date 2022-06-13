from django.core.management.base import BaseCommand

from basic.helper import recalculate_scout_hierarchy_child_model


class Command(BaseCommand):
    help = 'recalculate ScoutHierarchyChildModel'

    def handle(self, *args, **options):
        recalculate_scout_hierarchy_child_model()
