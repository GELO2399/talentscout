from django.urls import path
from .views import profile, employer_signup, employer_dashboard, employer_login, employer_job_detail, login_redirect, set_login_role, set_employer_login

app_name = 'users'

urlpatterns = [
    path('login-redirect/', login_redirect, name='login_redirect'),
    path('employer-dashboard/', employer_dashboard, name='employer_dashboard'),
    path('profile/', profile, name='profile'),
    path('employer-signup/', employer_signup, name='employer_signup'),
    path('employer-login/', employer_login, name='employer_login'),
    path('employer-job/<int:job_id>/', employer_job_detail, name='employer_job_detail'),
    path('set-login-role/', set_login_role, name='set_login_role'),
    path('set-employer-login/', set_employer_login, name='set_employer_login'),
]
