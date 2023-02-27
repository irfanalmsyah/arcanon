import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Room
from datetime import datetime
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        user = self.scope.get("user", None)
        if not user or not user.is_authenticated:
            await self.close()
            return
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        previous_messages = await self.get_previous_messages()
        for message in previous_messages:
            if message.user == user:
                await self.send(text_data=json.dumps({
                    "message": message.message, 
                    "user": "You",
                    "timestamp": message.created_at.strftime("%Y-%m-%d %H:%M:%S")
                }))
            else:
                await self.send(text_data=json.dumps({
                    "message": message.message, 
                    "user": "Stranger",
                    "timestamp": message.created_at.strftime("%Y-%m-%d %H:%M:%S")
                }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        try:
            message = text_data_json["message"]
            user = self.scope.get("user", None)
            if not user or not user.is_authenticated:
                await self.close()
                return
            message = await self.create_message(user, message)
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message", 
                    "message": message.message,
                    "user": message.user.username,
                    "timestamp": message.created_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            )
        except Exception as e:
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "destroy"
                }
            )

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        if user == self.scope.get("user", None).username:
            await self.send(text_data=json.dumps({"message": message, "user": "You"}))
        else:
            await self.send(text_data=json.dumps({"message": message, "user": "Stranger"}))

    async def destroy(self, event):
        await self.delete_room()
        await self.send(text_data=json.dumps({"destroy": 1}))

    @database_sync_to_async
    def get_previous_messages(self):
        room = Room.objects.get(name=self.room_name)
        return Message.objects.filter(room=room)
        
    @database_sync_to_async
    def create_message(self, user, message):
        room = Room.objects.get(name=self.room_name)
        return Message.objects.create(
            user=user,
            room=room,
            message=message
        )
    
    @database_sync_to_async
    def delete_room(self):
        room = Room.objects.get(name=self.room_name)
        room.delete()