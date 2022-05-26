from django.urls import include, path
from rest_framework_nested import routers

from . import views
from event.urls import router as event_router

router = routers.SimpleRouter()
router.register(r'available-templates', views.FileTemplateViewSet)

event_file_generator = routers.NestedSimpleRouter(event_router, r'event', lookup='event')
event_file_generator.register(r'files/generate', views.GenerateFilesViewSet, basename='generate-files')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('files/', include(router.urls)),
    path('', include(event_file_generator.urls)),
]
