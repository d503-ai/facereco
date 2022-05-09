from django.urls import path
from . import views
from .views import pageNotFound

urlpatterns = [
    path('', views.index, name='home'),
    path('detection/', views.detection, name='detection'),
    path('recognize/', views.recognize, name='recognize'),
    path('result_recon/', views.resultRecon, name='result-recon'),
    path('result_detect/', views.resultDetect, name='result-detect'),
]

