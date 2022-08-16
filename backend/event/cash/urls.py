from django.urls import include, path
from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()
router.register(r'income', views.CashIncomeViewSet)
router.register(r'mail-reminder', views.MailReminderViewSet, basename='mail-reminder')

urlpatterns = [
    path('', include(router.urls)),
]
