from rest_framework import status
from rest_framework.response import Response

from .models import Event


def get_dataset(kwargs, pk, dataset):
    dataset_id = kwargs.get(pk, None)
    if dataset_id is not None:
        return dataset.objects.filter(id=dataset_id)
    else:
        return Response('No dataset selected', status=status.HTTP_400_BAD_REQUEST)


def get_event(kwargs):
    event_id = kwargs.get("event_pk", None)
    if event_id is not None:
        return Event.objects.filter(id=event_id)
    else:
        return Response('No event selected', status=status.HTTP_400_BAD_REQUEST)
