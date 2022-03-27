from django.contrib import admin
from django.urls import path, include
from django_ses.views import SESEventWebhookView
from eb_sqs_worker.urls import urlpatterns as eb_sqs_urlpatterns
from eb_sqs_worker.views import HandleSQSTaskView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('basic/', include('basic.urls')),
    path('auth/', include('authentication.urls')),
    path('event/', include('event.urls')),
    path(r'ses/event-webhook/', SESEventWebhookView.as_view(), name='handle-event-webhook'),
    path(r'', HandleSQSTaskView.as_view(), name="sqs_handle")
]

