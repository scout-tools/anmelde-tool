from django.urls import include, path
from rest_framework_nested import routers

from . import views
from event.urls import router

event_summary_router = routers.NestedSimpleRouter(router, r'event', lookup='event')
event_summary_router.register(r'summary', views.EventSummaryViewSet, basename='summary')
event_summary_router.register(r'summary/detailed', views.EventDetailedSummaryViewSet, basename='detailed')
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
