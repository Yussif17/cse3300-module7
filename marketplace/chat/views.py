from django.shortcuts import render
from pymongo import MongoClient
from credentials import uri
from bson import ObjectId

client = MongoClient(uri)
database = client["marketplace"]
messages_collection = database["messages"]

def private_chat(request, user1, user2):
    room_name = f"chat_{'_'.join(sorted([user1, user2]))}"

    messages = list(messages_collection.find({"room": room_name}).sort("_id", 1))  

    return render(request, "chat/chat_box.html", {
        "user1": user1,
        "user2": user2,
        "messages": messages, 
    })