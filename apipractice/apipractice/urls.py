
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('watch/', include('apipractice_app.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
