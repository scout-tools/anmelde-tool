from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from email_services.services import send_custom_mail
from event import permissions as event_permissions
from event.email.serializers import CustomMailSerializer


# Create your views here.
class CustomMailViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsStaffOrReadOnly]
    serializer_class = CustomMailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event_id = kwargs.get("event_pk", None)
        send_custom_mail(event_id, serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
