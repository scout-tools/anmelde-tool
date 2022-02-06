# myapi/urls.py
from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register(r'event-location', views.EventLocationViewSet)
router.register(r'event', views.EventViewSet)
router.register(r'event-type-choices', views.RegistrationTypeViewSet, basename='event-type-choices')
router.register(r'event-planer-overview', views.EventPlanerViewSet, basename='event-planer-overview')

event_router = routers.NestedSimpleRouter(router, r'event', lookup='event')
event_router.register(r'sleeping-locations', views.SleepingLocationViewSet,
                      basename='sleeping-locations')

# registration_router = routers.NestedSimpleRouter(router, r'registration', lookup='registration')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(event_router.urls)),
]
