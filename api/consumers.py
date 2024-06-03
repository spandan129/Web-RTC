from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('ok')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(f"Connected to room: {self.room_name}") 

        try:
            await self.channel_layer.group_add(
                self.room_name,
                self.channel_name
            )
        except Exception as e:
            print(f"Error adding to group: {e}") 
            await self.close()  

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
        except json.JSONDecodeError as e:
            print(f"Invalid JSON data received: {e}")
            return  

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.group_name = f"group_{self.group_name}"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get('message')
            username = data.get('username')
            print(message)
            print(username)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON data received: {e}")
            return 

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                'message': message,
                'sent_by': username  
            }
        )

    async def group_message(self, event):
        message = event['message']
        sent_by = event.get('sent_by', 'Anonymous')  

        await self.send(text_data=json.dumps({
            'message': message,
            'sent_by': sent_by  
        }))

class CallConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            'type': 'connection',
            'data': {
                'message': "Connected"
            }
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)


        eventType = text_data_json['type']

        if eventType == 'login':
            name = text_data_json['data']['name']
            self.my_name = name
            
            async_to_sync(self.channel_layer.group_add)(
                self.my_name,
                self.channel_name
            )
        
        if eventType == 'call':
            name = text_data_json['data']['name']
            print('this is the name')
            async_to_sync(self.channel_layer.group_send)(
                name,
                {
                    'type': 'call_received',
                    'data': {
                        'caller': self.my_name,
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'answer_call':
            
            caller = text_data_json['data']['caller']
            async_to_sync(self.channel_layer.group_send)(
                caller,
                {
                    'type': 'call_answered',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'ICEcandidate':

            user = text_data_json['data']['user']

            async_to_sync(self.channel_layer.group_send)(
                user,
                {
                    'type': 'ICEcandidate',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }  
            )

    def call_received(self, event):
        print('Call received by ', self.my_name )
        self.send(text_data=json.dumps({
            'type': 'call_received',
            'data': event['data']
        }))


    def call_answered(self, event):

        print(self.my_name, "'s call answered")
        self.send(text_data=json.dumps({
            'type': 'call_answered',
            'data': event['data']
        }))


    def ICEcandidate(self, event):
     self.send(text_data=json.dumps({
        'type': 'ICEcandidate',
        'data': event['data']
    }))