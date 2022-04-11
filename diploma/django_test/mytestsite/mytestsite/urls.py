from django.contrib import admin
from django.urls import path, include

from websitre.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('websitre/', include('websitre.urls')),
]

handler404 = page_not_found