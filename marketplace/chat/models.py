from django.db import models

from pymongo import MongoClient
from credentials import uri


client = MongoClient(uri)
database = client["marketplace"]
messages_collection = database["messages"] 
