from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register(r'responsables', views.ResponsablePersonViewSet, basename='responsables')
router.register(r'personal-data', views.PersonalData, basename='personal-data')
router.register(r'personal-data-check', views.PersonalDataCheck, basename='personal-data-check')
router.register(r'groups', views.GroupViewSet, basename='groups')
router.register(r'person', views.PersonsViewSet, basename='person')
router.register(r'person-connect', views.PersonConnect, basename='person-connect')


router.register(r'email-settings', views.EmailSettingsViewSet, basename='email-settings')
router.register(r'email-notification-types', views.EmailNotificationTypeViewSet, basename='email-notification-types')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
