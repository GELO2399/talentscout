from django.urls import path
from .views import chat_view,start_conversation,conversation_detail,chat_dashboard

app_name = 'messaging'

urlpatterns = [
    path('chat/', chat_dashboard, name='chat'),
    path('start_conversation/<int:user_id>/', start_conversation, name='start_conversation'),
    path('conversation/<int:conversation_id>/', conversation_detail, name='conversation_detail'),
    path('chat/<int:conversation_id>/', chat_view, name='chat_view'),
]
