import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Room
from main.models import User
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
        identity = await self.get_identity(user)
        if identity:
            await self.send(text_data=json.dumps({
                "type": "identity",
                "name": identity.name,
                "country": identity.country,
                "instagram": identity.instagram,
                "twitter": identity.twitter,
                "picture": identity.picture.url if identity.picture else None
            }))
        previous_messages = await self.get_previous_messages()
        for message in previous_messages:
            if message.user == user:
                await self.send(text_data=json.dumps({
                    "type": "message",
                    "message": message.message, 
                    "user": "You",
                    "timestamp": message.created_at.strftime("%Y-%m-%d %H:%M:%S")
                }))
            else:
                await self.send(text_data=json.dumps({
                    "type": "message",
                    "message": message.message, 
                    "user": "Stranger",
                    "timestamp": message.created_at.strftime("%Y-%m-%d %H:%M:%S")
                }))
                

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json["type"]
        if type == "message":
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
        elif type == "destroy":
            await self.delete_room()
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "destroy"
                }
            )
        elif type == "reveal_request":
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "reveal_request",
                    "user": text_data_json["user"]
                }
            )
        elif type == "reveal_response":
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "reveal_response",
                    "user": text_data_json["user"],
                    "reveal": text_data_json["reveal"]
                }
            )

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        if user == self.scope.get("user", None).username:
            await self.send(text_data=json.dumps({
                "type": "message",
                "message": message,
                "user": "You"
            }))
        else:
            await self.send(text_data=json.dumps({
                "type": "message",
                "message": message,
                "user": "Stranger"
            }))

    async def destroy(self, event):
        await self.send(text_data=json.dumps({
            "type": "destroy",
        }))
    
    async def reveal_request(self, event):
        user = User.objects.get(username=event["user"])
        room = Room.objects.get(name=self.room_name)
        complete = user.isComplete()

        if not complete:
            if event["user"] == self.scope.get("user", None).username:
                await self.send(text_data=json.dumps({
                    "type": "reveal_request_you_not_complete",
                }))
            return
        
        if user == room.requester:
            complete = room.responder.isComplete()
        else:
            complete = room.requester.isComplete()
        
        if not complete:
            if event["user"] == self.scope.get("user", None).username:
                await self.send(text_data=json.dumps({
                    "type": "reveal_request_stranger_not_complete",
                }))
            return
        
        if event["user"] != self.scope.get("user", None).username:
            await self.send(text_data=json.dumps({
                "type": "reveal_request",
            }))
    
    async def reveal_response(self, event):
        if event["reveal"]:
            user = self.scope.get("user", None)
            await self.reveal_room()
            identity = await self.get_identity(user)
            if identity:
                await self.send(text_data=json.dumps({
                    "type": "identity",
                    "name": identity.name,
                    "country": identity.country,
                    "instagram": identity.instagram,
                    "twitter": identity.twitter,
                    "picture": identity.picture.url if identity.picture else None
                }))
        else:
            if event["user"] != self.scope.get("user", None).username:
                await self.send(text_data=json.dumps({
                    "type": "reveal_response_rejected",
                }))

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
    
    @database_sync_to_async
    def reveal_room(self):
        room = Room.objects.get(name=self.room_name)
        room.reveal = True
        room.save()
    
    @database_sync_to_async
    def get_identity(self, user):
        room = Room.objects.get(name=self.room_name)
        if room.reveal:
            if user == room.requester:
                return room.responder
            else:
                return room.requester
        else:
            return None