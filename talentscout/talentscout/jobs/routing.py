from django.urls import path,re_path
from . import consumers

websocket_urlpatterns = [
    path('ws/jobs/<int:job_id>/', consumers.JobApplicationConsumer.as_asgi()),
    re_path(r'ws/applicant_dashboard/(?P<user_id>\d+)/$', consumers.ApplicantDashboardConsumer.as_asgi()),
]