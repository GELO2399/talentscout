# jobs/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class JobApplicationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.job_id = self.scope['url_route']['kwargs']['job_id']
        self.group_name = f'job_{self.job_id}'

        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        status = data['status']
        applicant = data['applicant']

        # Send message to the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'status_update',
                'status': status,
                'applicant': applicant
            }
        )

    # Receive message from group
    async def status_update(self, event):
        status = event['status']
        applicant = event['applicant']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'status': status,
            'applicant': applicant
        }))
class ApplicantDashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # The group name is dynamic based on the user
        self.group_name = f"applicant_{self.scope['user'].id}"

        # Join the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def application_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'application_update',
            'message': event['message'],
            'status': event['status'],
            'job_id': event['job_id']
        }))

class JobConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.job_id = self.scope['url_route']['kwargs']['job_id']
        self.room_group_name = f'job_{self.job_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f"Connected to job {self.job_id}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"Disconnected from job {self.job_id}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        application_id = data.get('id')
        status = data.get('status')
        
        # Send update to the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'status_update',
                'id': application_id,
                'status': status,
            }
        )

    async def status_update(self, event):
        await self.send(text_data=json.dumps(event))
