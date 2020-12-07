from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.OneClickView.as_view()),
    path('token/', TokenObtainPairView.as_view(serializer_class=views.MyTokenObtainPairSerializer))

]
