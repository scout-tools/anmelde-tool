from django.urls import include, path
from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()


urlpatterns = [
    path('', include(router.urls)),
]
