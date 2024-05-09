import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async 
from asgiref.sync import async_to_sync
import jwt
from django.conf import settings
from user.models import UserAccount
from channels.layers import get_channel_layer

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # access_token = self.scope['url_route']['kwargs']['access_token']
        self.room_group_name = f"chat_{self.room_name}"
        self.user = None
        

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        access_token = text_data_json["access_token"]
        receiver = text_data_json["receiver"]
        print("The token : ",access_token)
        try:
            decoded_token =jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            # user = await sync_to_async(UserAccount.objects.get)(id=decoded_token['user_id'])
            user = await sync_to_async(UserAccount.objects.get)(id=decoded_token['user_id'])
           
            print("The user is : ",user)
            # Now you have the user object, do whatever you need with it
        except jwt.ExpiredSignatureError:
            # Handle token expiration error
            print("error")
            pass
        except jwt.InvalidTokenError:
            # Handle invalid token error
            print("error")
            pass
        
        if user:
            new_message = await sync_to_async(ChatMessage.objects.create)(
                room_name=self.room_name,
                sender=user,
                message=message
            )
            
            
            message_data = {
                'id': new_message.id,  # Include the message ID
                'sender': user.id,  
                'receiver': receiver,
                "room_name": self.room_name,
                'message': new_message.message,
                'timestamp': str(new_message.timestamp),  # Convert timestamp to string
            }
            print("the user name is : ", user.id,   user.fullname())
            self.username = user.fullname()

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": message_data}
            )
            print("successfully completed")

            # Send notification to notification group
            await self.send_notification(message_data)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
        
    async def send_notification(self, message_data):
        # Get the channel layer
        channel_layer = get_channel_layer()

        # Construct the notification message
        notification_message = {
            "type": "notification.message",
            "message": message_data["message"],
            "sender": self.username,
            "timestamp": message_data["timestamp"]
        }
        
        # Construct the group name with user.id
        group_name = f"chat_link{message_data['receiver']}"
        print("the groupname is", group_name)
        print('sending notification')
        print("message data : ", message_data)
        # Send the notification message to the notification group
        await channel_layer.group_send(
            group_name,
            notification_message
        )
        print('notificaion sent :', notification_message)
        
        
        
        
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = None
        
        # Join the notification group
        print("connecting to the room and the room group name is", self.room_group_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the notification group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    async def notification_message(self, event):
        # Send message to WebSocket
        print("sending notificaion to the frontend")
        message = {
                    
                  }
        await self.send(text_data=json.dumps({
            'payload': event['message'],
            "sender": event['sender'],
            "type": event['type']
            
        }))
        