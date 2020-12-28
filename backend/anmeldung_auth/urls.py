from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'user-extended', views.UserExtendedViewSet)

urlpatterns = [
    path('data/', include(router.urls)),
    path('authenticate/', views.AuthenticateView.as_view()),
    path('token/', TokenObtainPairView.as_view(serializer_class=views.MyTokenObtainPairSerializer))
]
