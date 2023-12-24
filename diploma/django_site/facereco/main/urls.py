from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('recognize/', views.recognize, name='recognize'),
    path('result_recon/<int:record_id>/', views.resultRecon, name='result-recon'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('record_details/<int:record_id>/', views.record_details, name='record-details'),
    path('test/<int:record_id>/', views.test, name='test'),
]

