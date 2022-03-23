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
# router.register(r'event-module-mapper', views.EventModulesMapperViewSet, basename='eventmodulemapper')
router.register(r'event-overview', views.EventOverviewViewSet, basename='event-overview')
router.register(r'event-registration', views.EventRegistrationViewSet, basename='event-registration')
router.register(r'registration', views.RegistrationViewSet, basename='registration')
router.register(r'gender-choices', views.GenderViewSet, basename='gender-choices')

event_router = routers.NestedSimpleRouter(router, r'event', lookup='event')
event_router.register(r'booking-options', views.BookingOptionViewSet, basename='booking-options')
event_router.register(r'assigned-event-modules', views.AssignedEventModulesViewSet, basename='assigned-event-modules')
event_router.register(r'available-modules', views.AvailableEventModulesViewSet, basename='available-modules')
event_router.register(r'event-module-mapper', views.EventModulesMapperViewSet, basename='eventmodulemapper')

event_module_router = routers.NestedSimpleRouter(event_router, r'event-module-mapper', lookup='eventmodulemapper')
event_module_router.register(r'attribute-mapper', views.EventModuleAttributeMapperViewSet, basename='attribute-mapper')

registration_router = routers.NestedSimpleRouter(router, r'registration', lookup='registration')
registration_router.register(r'single-participant', views.RegistrationSingleParticipantViewSet,
                             basename='single-participant')
registration_router.register(r'group-participants', views.RegistrationGroupParticipantViewSet,
                             basename='group-participants')
registration_router.register(r'attribute', views.RegistrationAttributeViewSet, basename='attribute')
registration_router.register(r'summary', views.RegistrationSummaryViewSet, basename='summary')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(event_router.urls)),
    path('', include(event_module_router.urls)),
    path('', include(registration_router.urls)),
]
