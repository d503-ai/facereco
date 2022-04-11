from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/<int:webid>/', about, name='about')
]
