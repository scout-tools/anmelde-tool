from django.db.models import QuerySet
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from event.file_generator.models import GeneratedFiles, FileTemplate
from event.file_generator.serializers import GeneratedFilesGetSerializer, GeneratedFilesPostSerializer, \
    FileTemplateSerializer
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
        file_type = self.request.query_params.getlist('file-type')
        status = self.request.query_params.getlist('status')
        generated = GeneratedFiles.objects.filter(event=event_id)
        if file_type:
            generated = generated.filter(template__in=file_type)
        if status:
            generated = generated.filter(status__in=status)
        return generated.order_by('-created_at', 'updated_at')

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return GeneratedFilesPostSerializer
        else:
            return GeneratedFilesGetSerializer


class FileTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FileTemplateSerializer
    queryset = FileTemplate.objects.all()
