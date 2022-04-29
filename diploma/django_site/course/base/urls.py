from django.urls import path
from . import views

# CONNECTING BASE'S URLS TO BASE'S VIEWS. MAKE
# THEM TO BE SEPARATE FROM EACH OTHER
urlpatterns = [
    path('', views.home, name="home"),
    path('room/<str:pk>', views.room, name="room"),
]