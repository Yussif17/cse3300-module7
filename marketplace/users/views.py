from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password, check_password
from pymongo import MongoClient
from credentials import uri
from bson import ObjectId

client = MongoClient(uri)
# Create your views here.

def register_view(request):
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user) #form.save() returns user value
      new_user = {
        "_id": ObjectId(),
        "username": user.username,
        "email": user.email,
        "password": make_password(request.POST["password1"]),
      }
      database= client["marketplace"]
      collection = database["users"]
      collection.insert_one(new_user)
      return redirect("posts:list") #name of app then named
  else:
    form = UserCreationForm()
  return render(request, 'users/register.html', { "form":form })

def login_view(request):
  if request.method == "POST":
    database= client["marketplace"]
    collection = database["users"]
    username = request.POST["username"]
    password = request.POST["password"]
    user = collection.find_one({"username": username})

    if user and check_password(password, user["password"]): 
      request.session["user_id"] = str(user["_id"])
      request.session["username"] = user["username"]
      if "next" in request.POST:
        return redirect(request.POST.get("next"))
      return redirect("posts:list")
    
    return render(request, "users/login.html", {"error": "Invalid username or password"})
  return render(request, "users/login.html")

def logout_view(request):
  if request.method == "POST":
    logout(request)
    return (redirect("posts:home"))