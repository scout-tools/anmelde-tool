from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register(r'personal-data', views.PersonalData, basename='personal-data')
router.register(r'personal-data-check', views.PersonalDataCheck, basename='personal-data-check')
router.register(r'groups', views.GroupViewSet, basename='groups')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]