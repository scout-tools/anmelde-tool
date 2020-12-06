# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'event', views.EventViewSet)
router.register(r'age-group', views.AgeGroupViewSet)
router.register(r'event-location', views.EventLocationViewSet)
router.register(r'person', views.PersonViewSet)
router.register(r'scout-herarchy', views.ScoutHerarchyViewSet)
router.register(r'registration', views.RegistrationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('basic/', include(router.urls)),
]
