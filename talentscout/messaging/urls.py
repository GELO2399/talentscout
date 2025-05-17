from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('<int:receiver_id>/', views.message_list, name='message_list'),
]
