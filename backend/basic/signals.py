from basic.helper import recalculate_scout_hierarchy_child_model
from basic.models import ScoutHierarchy


def post_save_scout_hierarchy(sender: ScoutHierarchy, instance: ScoutHierarchy, update_fields, raw, **kwargs):
    recalculate_scout_hierarchy_child_model()
