from django.contrib import admin
from django.urls import path, include
from django_ses.views import SESEventWebhookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('basic/', include('basic.urls')),
    path('auth/', include('authentication.urls')),
    path('event/', include('event.urls')),
    path(r'ses/event-webhook/', SESEventWebhookView.as_view(), name='handle-event-webhook'),
]

