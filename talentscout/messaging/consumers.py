import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender']

        # Save message to DB asynchronously
        await self.save_message(self.conversation_id, sender_id, message)

        # Broadcast message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': await self.get_username(sender_id),
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
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
