# messaging/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from users.models import UserProfile
from django.contrib.auth.models import User
from django.utils import timezone


@login_required
def start_conversation(request, user_id):
    """Start or fetch an existing conversation with the user."""
    user = get_object_or_404(User, id=user_id)

    # Check if a conversation already exists
    conversation, created = Conversation.objects.get_or_create()
    if not created:
        conversation.participants.add(request.user, user)
    
    return redirect('messaging:conversation_detail', conversation_id=conversation.id)


@login_required
def conversation_detail(request, conversation_id):
    """Display the conversation details and handle message sending."""
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    messages = conversation.messages.order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content,
                timestamp=timezone.now()
            )
            return redirect('messaging:conversation_detail', conversation_id=conversation.id)

    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
    })


def chat_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    return render(request, 'messaging/chat.html', {
        'conversation': conversation,
        'user': request.user
    })

def chat_dashboard(request):
    return render(request, 'messaging/chat_dashboard.html')