from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('chat/', views.chat_inbox, name='chat'),
    path('<int:receiver_id>/', views.message_list, name='message_list'),
    path('chat/start/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('chat/<int:conversation_id>/', views.chat_view, name='chat_detail'),

]
