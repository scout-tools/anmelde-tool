from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'user-extended', views.UserExtendedViewSet)

urlpatterns = [
    path('data/', include(router.urls)),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.OneClickView.as_view()),
    path('token/', TokenObtainPairView.as_view(serializer_class=views.MyTokenObtainPairSerializer))
]
