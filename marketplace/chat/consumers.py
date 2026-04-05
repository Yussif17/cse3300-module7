# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from pymongo import MongoClient
# from credentials import uri

# client = MongoClient(uri)
# database = client["marketplace"]
# messages_collection = database["messages"]

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):

#         self.user1 = self.scope["url_route"]["kwargs"]["user1"]
#         self.user2 = self.scope["url_route"]["kwargs"]["user2"]

#         self.room_name = f"chat_{'_'.join(sorted([self.user1, self.user2]))}"
#         self.room_group_name = f"chat_{self.room_name}"

#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     async def receive(self, text_data):
#         try:
#             data = json.loads(text_data)


#             message = data.get("message", "").strip()
#             sender = data.get("sender", "").strip()

#             if not message or not sender:
#                 return  

#             chat_message = {
#                 "room": self.room_name,
#                 "sender": sender,
#                 "message": message,
#             }
#             messages_collection.insert_one(chat_message)  

#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     "type": "chat_message",
#                     "message": message,
#                     "sender": sender,
#                 },
#             )

#         except json.JSONDecodeError:
#             print("Error: Invalid JSON received in WebSocket")

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             "message": event["message"],
#             "sender": event["sender"],
#         }))

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from pymongo import MongoClient
from credentials import uri

client = MongoClient(uri)
database = client["marketplace"]
messages_collection = database["messages"]

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Establish WebSocket connection."""
        self.user1 = self.scope["url_route"]["kwargs"]["user1"]
        self.user2 = self.scope["url_route"]["kwargs"]["user2"]
        self.room_name = f"chat_{'_'.join(sorted([self.user1, self.user2]))}"
        self.room_group_name = f"chat_{self.room_name}"

        print(f"✅ [WebSocket] Connection Attempt: {self.user1} <-> {self.user2}") 

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print(f"✅ [WebSocket] Connected to Room: {self.room_group_name}")

    async def disconnect(self, close_code):
        """Remove user from the WebSocket room."""
        print(f"❌ [WebSocket] Disconnected: {self.user1} <-> {self.user2}")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Receive a message from WebSocket, store it in MongoDB, and broadcast it."""
        print(f"📩 [WebSocket] Message Received: {text_data}")

        data = json.loads(text_data)
        message = data.get("message", "").strip()
        sender = data.get("sender", "").strip()

        if not message or not sender:
            print("⚠️ [WebSocket] Invalid message received")
            return  # Ignore empty messages

        chat_message = {
            "room": self.room_name,
            "sender": sender,
            "message": message,
        }
        messages_collection.insert_one(chat_message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
            },
        )

    async def chat_message(self, event):
        """Send received message to WebSocket clients."""
        print(f"📤 [WebSocket] Sending message: {event['message']} from {event['sender']}")
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))