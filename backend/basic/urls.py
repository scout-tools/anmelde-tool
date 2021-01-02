# myapi/urls.py
from django.urls import include, path
from rest_framework_nested import routers


from . import views

router = routers.SimpleRouter()
router.register(r'event', views.EventViewSet)
router.register(r'age-group', views.AgeGroupViewSet)
router.register(r'event-location', views.EventLocationViewSet)
router.register(r'scout-hierarchy', views.ScoutHierarchyViewSet)
router.register(r'registration', views.RegistrationViewSet)
router.register(r'zip-code', views.ZipCodeViewSet)
router.register(r'participant', views.ParticipantViewSet)

event_router = routers.NestedSimpleRouter(router, r'event', lookup='event')
event_router.register(r'participants', views.ParticipantViewSet2, basename='event-participants')

router.register(r'zip-code', views.ZipCodeViewSet)
router.register(r'participant-extended', views.ParticipantExtendedViewSet)
router.register(r'participant-role', views.ParticipantRoleViewSet)
router.register(r'eat-habit-type', views.EatHabitTypeViewSet)
router.register(r'eat-habit', views.EatHabitViewSet)
router.register(r'travel-type', views.TravelTypeViewSet)
router.register(r'tent-type', views.TentTypeViewSet)
router.register(r'tent', views.TentViewSet)
router.register(r'scout-orga-level', views.ScoutOrgaLevelViewSet)
router.register(r'role', views.RoleViewSet)
router.register(r'method-of-travel', views.MethodOfTravelViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('basic/', include(router.urls)),
    path('basic/', include(event_router.urls)),
]
