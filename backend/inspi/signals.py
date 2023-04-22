from django.db.models import Sum

from inspi import models as inspi_models


def post_save_like(sender: inspi_models.Like, instance: inspi_models.Like, update_fields, raw, **kwargs):
    if instance.id:
        query = inspi_models.Like.objects.filter(event=instance.event).all().aggregate(sum=Sum('opinion_type_id'))
        likes = query['sum']

        if likes is None:
            likes = 0

        if likes < 3:
            like_score = 0
        elif likes < 10:
            like_score = 1
        elif likes < 20:
            like_score = 2
        elif likes >= 20:
            like_score = 3
        else:
            like_score = 0

        event = inspi_models.Activity.objects.filter(id=instance.event.id).first()
        event.like_score = like_score
        event.save()
