from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('post/', views.post_job, name='post_job'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('<int:job_id>/', views.employer_job_detail, name='employer_job_detail'),
    path('accept/<int:application_id>/', views.accept_application, name='accept_application'),
    path('reject/<int:application_id>/', views.reject_applicant, name='reject_applicant'),
]
