from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message
from .forms import MessageForm
from django.contrib.auth import get_user_model

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
<<<<<<< HEAD


def chat_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    return render(request, 'messaging/chat.html', {
        'conversation': conversation,
        'user': request.user
    })

def chat_dashboard(request):
    return render(request, 'messaging/chat_dashboard.html')
=======
>>>>>>> parent of 4094cd6f (Addition of Messaging and Chat, Development is on progress)
