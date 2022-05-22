from django.urls import include, path
from rest_framework_nested import routers

from . import views
from event.urls import router

event_file_generator = routers.NestedSimpleRouter(router, r'event', lookup='event')
event_file_generator.register(r'files', views.GenerateFilesViewSet, basename='generate-files')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(event_file_generator.urls)),
]
