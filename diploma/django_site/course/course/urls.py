from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # IMPORT URLS FROM BASE, SO IT'S DEFAULT PATH
    path('', include('base.urls')),
]
