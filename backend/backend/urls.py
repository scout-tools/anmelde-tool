from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('basic/', include('basic.urls')),
    path('auth/', include('authentication.urls')),
    path('event/', include('event.urls'))
]
