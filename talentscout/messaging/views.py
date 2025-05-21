from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message, Conversation
from .forms import MessageForm
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()

@login_required
def message_list(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('messaging:message_list', receiver_id=receiver_id)
    else:
        form = MessageForm()

    return render(request, 'messaging/message_list.html', {
        'messages': messages,
        'receiver': receiver,
        'form': form,
    
    })
def chat_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    return render(request, 'messaging/chat.html', {'conversation': conversation})

@login_required
def start_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # Try to get an existing conversation with both users
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()

    # If not found, create it
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.set([request.user, other_user])
        conversation.save()

    return redirect('chat', conversation_id=conversation.id)
@login_required
def chat_inbox(request):
    conversations = Conversation.objects.filter(participants=request.user)
    return render(request, 'messaging/inbox.html', {'conversations': conversations})