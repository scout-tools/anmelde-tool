from django.urls import include, path
from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()
router.register('registration', views.RegistrationViewSet, basename='registration')

registration_router = routers.NestedSimpleRouter(router, r'registration', lookup='registration')
registration_router.register(r'single-participant', views.RegistrationSingleParticipantViewSet,
                             basename='single-participant')
registration_router.register(r'group-participants', views.RegistrationGroupParticipantViewSet,
                             basename='group-participants')
registration_router.register(r'attribute', views.RegistrationAttributeViewSet, basename='attribute')
registration_router.register(r'summary', views.RegistrationSummaryViewSet, basename='summary')
registration_router.register(r'workshop', views.WorkshopViewSet, basename='workshop')
registration_router.register(r'add-reponsable', views.AddResponsablePersonRegistrationViewSet, basename='add-reponsable')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(registration_router.urls)),
]
