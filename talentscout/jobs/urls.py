from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('post/', views.post_job, name='post_job'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job/apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('employer/job/<int:job_id>/manage/', views.employer_job_detail, name='employer_job_detail'),
]
