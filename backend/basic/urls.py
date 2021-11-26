# myapi/urls.py
from django.urls import include, path
from rest_framework_nested import routers

router = routers.SimpleRouter()
# event_router = routers.NestedSimpleRouter(router, r'event', lookup='event')
# registration_router = routers.NestedSimpleRouter(router, r'registration', lookup='registration')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('basic/', include(router.urls)),
    # path('basic/', include(event_router.urls)),
    # path('basic/', include(registration_router.urls))
]
