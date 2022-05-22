from django.db.models import QuerySet
from rest_framework import mixins, viewsets

from event.file_generator.models import GeneratedFiles
from event.file_generator.serializers import GeneratedFilesGetSerializer, GeneratedFilesPostSerializer
from event.permissions import IsSubEventResponsiblePerson


# Create your views here.
class GenerateFilesViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsSubEventResponsiblePerson]

    def create(self, request, *args, **kwargs):
        request.data['event'] = kwargs.get("event_pk", None)
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[GeneratedFiles]:
        event_id = self.kwargs.get("event_pk", None)
        return GeneratedFiles.objects.filter(event=event_id).order_by('created_at', 'updated_at')

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return GeneratedFilesPostSerializer
        else:
            return GeneratedFilesGetSerializer
