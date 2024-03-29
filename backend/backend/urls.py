from django.contrib import admin
from django.urls import path, include

from . import index

urlpatterns = [
    path('', index.RedirectView.as_view()),
    path('admin/', admin.site.urls),
    path('basic/', include('basic.urls')),
    path('auth/', include('authentication.urls')),
    path('event/', include('event.urls')),
]
