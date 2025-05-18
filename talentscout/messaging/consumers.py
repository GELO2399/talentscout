import json
from channels.generic.websocket import AsyncWebsocketConsumer
<<<<<<< HEAD
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
=======
>>>>>>> parent of 4094cd6f (Addition of Messaging and Chat, Development is on progress)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_global'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
<<<<<<< HEAD
        sender_id = data['sender']

        # Save message to DB asynchronously
        await self.save_message(self.conversation_id, sender_id, message)

=======
        username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"

>>>>>>> parent of 4094cd6f (Addition of Messaging and Chat, Development is on progress)
        # Broadcast message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
<<<<<<< HEAD
                'sender': await self.get_username(sender_id),
=======
                'username': username
>>>>>>> parent of 4094cd6f (Addition of Messaging and Chat, Development is on progress)
            }
        )

    async def chat_message(self, event):
<<<<<<< HEAD
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
=======
>>>>>>> parent of 4094cd6f (Addition of Messaging and Chat, Development is on progress)
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))

    @database_sync_to_async
    def save_message(self, conversation_id, sender_id, message):
        from .models import Conversation, Message  # import here to avoid app loading issues
        conversation = Conversation.objects.get(id=conversation_id)
        sender = User.objects.get(id=sender_id)
        Message.objects.create(conversation=conversation, sender=sender, content=message)

    @database_sync_to_async
    def get_username(self, user_id):
        user = User.objects.get(id=user_id)
        return user.username
