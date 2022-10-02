from django.urls import include, path
from rest_framework_nested import routers

from event.urls import router
from . import views

event_mail_router = routers.NestedSimpleRouter(router, r'event', lookup='event')
event_mail_router.register(r'email/custom-mail', views.CustomMailViewSet, basename='custom-mail')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(event_mail_router.urls)),
]
