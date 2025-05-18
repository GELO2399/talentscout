from django.urls import path
from . import views

app_name = 'employers'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('applicants/', views.applicant_list, name='applicant_list'),
]
