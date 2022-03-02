# myapi/urls.py
from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register(r'event-location', views.EventLocationViewSet)
router.register(r'event', views.EventViewSet)
router.register(r'event-type-group-choices', views.RegistrationTypeGroupViewSet, basename='event-group-choices')
router.register(r'event-type-single-choices', views.RegistrationTypeSingleViewSet, basename='event-type-single-choices')
router.register(r'event-planer-overview', views.EventPlanerViewSet, basename='event-planer-overview')
router.register(r'event-module', views.EventModulesViewSet, basename='eventmodule')
router.register(r'event-module-mapper', views.EventModulesMapperViewSet, basename='eventmodulemapper')
router.register(r'event-overview', views.EventOverviewViewSet, basename='event-overview')

event_router = routers.NestedSimpleRouter(router, r'event', lookup='event')
event_router.register(r'sleeping-locations', views.SleepingLocationViewSet,
                      basename='sleeping-locations')
event_router.register(r'available-modules', views.AvailableEventModulesViewSet,
                      basename='available-modules')

event_module_router = routers.NestedSimpleRouter(router, r'event-module-mapper', lookup='eventmodulemapper')
event_module_router.register(r'attribute-mapper', views.EventModuleAttributeMapperViewSet,
                             basename='attribute-mapper')
# event_module_router.register(r'attributes', views.EventModuleAttributeViewSet,
#                              basename='attributes')

# registration_router = routers.NestedSimpleRouter(router, r'registration', lookup='registration')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(event_router.urls)),
    path('', include(event_module_router.urls)),
]
