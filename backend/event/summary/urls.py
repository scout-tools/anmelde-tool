from django.urls import include, path
from rest_framework_nested import routers

from event.urls import router
from . import views
from .kpi import views as kpi_views

event_summary_router = routers.NestedSimpleRouter(router, r'event', lookup='event')
event_summary_router.register(r'summary', views.EventSummaryViewSet, basename='summary')
event_summary_router.register(r'summary/age-groups', views.EventAgeGroupsSummaryViewSet, basename='age-groups')
event_summary_router.register(r'summary/leader-types', views.EventLeaderTypesSummaryViewSet, basename='leaderTypes')

event_summary_router.register(r'summary/kpi/total-participants', kpi_views.TotalParticipantsViewSet,
                              basename='total-participants')
event_summary_router.register(r'summary/kpi/total-registrations', kpi_views.TotalRegistrationsViewSet,
                              basename='total-participants')
event_summary_router.register(r'summary/kpi/last-registrations', kpi_views.LastRegistrationsViewSet,
                              basename='last-registrations')
event_summary_router.register(r'summary/kpi/largest-registrations', kpi_views.LargestRegistrationsViewSet,
                              basename='largest-registrations')
event_summary_router.register(r'summary/kpi/booking-options', kpi_views.BookingOptionViewSet,
                              basename='booking-options')

event_summary_router.register(r'summary/participant-locations', views.RegistrationLocationViewSet,
                              basename='participant-locations')
event_summary_router.register(r'summary/event-location', views.EventLocationViewSet, basename='event-location')
event_summary_router.register(r'summary/detailed', views.EventDetailedSummaryViewSet, basename='detailed')
event_summary_router.register(r'summary/staemme', views.RegistrationStaemmeViewSet, basename='detailed')
event_summary_router.register(r'summary/workshop', views.WorkshopEventSummaryViewSet, basename='workshop')
event_summary_router.register(r'summary/attributes', views.EventAttributeSummaryViewSet, basename='attributes')
event_summary_router.register(r'summary/food', views.EventFoodSummaryViewSet, basename='food')
event_summary_router.register(r'summary/cash', views.CashSummaryViewSet, basename='cash')
event_summary_router.register(r'summary/emails/responsible-persons', views.EmailResponsiblePersonsViewSet,
                              basename='emails-responsible-persons')
event_summary_router.register(r'summary/emails/registration-responsible-persons',
                              views.EmailRegistrationResponsiblePersonsViewSet,
                              basename='emails-registration-responsible-persons')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(event_summary_router.urls)),
]
