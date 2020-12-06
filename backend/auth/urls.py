from django.urls import include, path

from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.OneClickView.as_view()),
]
