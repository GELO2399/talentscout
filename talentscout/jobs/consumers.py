import json
from channels.generic.websocket import AsyncWebsocketConsumer

class JobConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.job_id = self.scope['url_route']['kwargs']['job_id']
        self.group_name = f'job_{self.job_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'status_update':
            # Broadcast status update to group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'status_update',
                    'id': data['id'],
                    'status': data['status'],
                }
            )

    # Receive message from room group
    async def status_update(self, event):
        await self.send(text_data=json.dumps({
            'action': 'status_update',
            'id': event['id'],
            'status': event['status'],
        }))
