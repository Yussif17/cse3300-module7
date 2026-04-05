from pymongo import MongoClient
from bson import ObjectId
from credentials import uri

client = MongoClient(uri)
database = client["marketplace"]
users_collection = database["users"]

def user_context(request):
    user_id = request.session.get("user_id")

    if user_id:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return {"authenticated_user": user} 

    return {"authenticated_user": None}