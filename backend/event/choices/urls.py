from django.urls import include, path
from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()
router.register(r'event-type-group', views.RegistrationTypeGroupViewSet, basename='event-type-group')
router.register(r'event-type-single', views.RegistrationTypeSingleViewSet, basename='event-type-single')
router.register(r'gender', views.GenderViewSet, basename='gender')
router.register(r'leader-types', views.LeaderTypesViewSet, basename='leader-types')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
