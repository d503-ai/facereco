from django.urls import path
from . import views
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

urlpatterns = [
    path('', views.index, name='home'),
    path('recognize/', views.recognize, name='recognize'),
    path('result_recon/<int:record_id>/', views.resultRecon, name='result-recon'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('record_details/<int:record_id>/', views.record_details, name='record-details'),
    path('select_faces/<int:record_id>/', views.select_faces, name='select-faces'),
    path('delete_record/<int:record_id>/', views.delete_record, name='delete-record'),
]