from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register(r'event-location', views.EventLocationViewSet)
router.register(r'event', views.EventViewSet)
router.register(r'event-planer-overview', views.EventPlanerViewSet, basename='event-planer-overview')
router.register(r'event-statistics-overview', views.EventStatisticsViewSet, basename='event-statistics-overview')
router.register(r'event-module', views.EventModulesViewSet, basename='event-module')
router.register(r'event-overview', views.EventOverviewViewSet, basename='event-overview')
router.register(r'event-registration', views.EventRegistrationViewSet, basename='event-registration')
router.register(r'registration-scouthierarchy', views.ScoutHierarchyViewSet, basename='registration-scouthierarchy')

event_router = routers.NestedSimpleRouter(router, r'event', lookup='event')
event_router.register(r'booking-options', views.BookingOptionViewSet, basename='booking-options')
event_router.register(r'assigned-event-modules', views.AssignedEventModulesViewSet, basename='assigned-event-modules')
event_router.register(r'available-modules', views.AvailableEventModulesViewSet, basename='available-modules')
event_router.register(r'event-module-mapper', views.EventModulesMapperViewSet, basename='eventmodulemapper')

event_module_router = routers.NestedSimpleRouter(event_router, r'event-module-mapper', lookup='eventmodulemapper')
event_module_router.register(r'attribute-mapper', views.EventModuleAttributeMapperViewSet, basename='attribute-mapper')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(event_router.urls)),
    path('', include(event_module_router.urls)),
    path('', include('event.registration.urls')),
    path('', include('event.summary.urls')),
    path('choices/', include('event.choices.urls')),
    path('cash/', include('event.cash.urls')),
    path('', include('event.file_generator.urls')),
    path('', include('event.email.urls'))
]
