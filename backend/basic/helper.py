from basic.models import ScoutHierarchy, ScoutHierarchyChildModel


def recalculate_scout_hierarchy_child_model():
    ScoutHierarchyChildModel.objects.all().delete()

    for i in range(5, 1, -1):
        level = ScoutHierarchy.objects.filter(level__id=i)

        for tmp in level:
            child_model = ScoutHierarchyChildModel(head=tmp)
            child_model.save()
            child_model.childs.add(tmp)
            tmp_childs = ScoutHierarchyChildModel.objects.filter(head__in=tmp.scouthierarchy.all())
            for ring_child in tmp_childs:
                child_model.childs.add(*ring_child.childs.all())
                child_model.childs.add(ring_child.head)
