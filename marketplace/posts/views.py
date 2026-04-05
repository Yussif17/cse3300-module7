from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from . import forms
from pymongo import MongoClient
import os
from datetime import datetime, timezone,timedelta
from bson import ObjectId
from credentials import uri
import gridfs
from django.http import HttpResponse
from . import forms
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
client = MongoClient(uri)


def home_page(request):
  return render(request, 'home.html')

def posts_list(request):
  posts = list(client["marketplace"]["posts"].find())
  posts.reverse()
  for post in posts:
    if "image" in post and isinstance(post["image"], ObjectId):
      post["image_id"] = str(post["image"])
    else:
      post["image_id"] = None 
  return render(request, 'posts/posts_list.html', { 'posts': posts})

def post_page(request, slug):
  database = client["marketplace"]
  collection = database["posts"]
  post = collection.find_one({"slug": slug})  
  if not post:
    return HttpResponse("Post not found", status=404)
  if "image" in post and post["image"]:
    post["image_id"] = str(post["image"]) 
  else:
    post["image_id"] = None 
  return render(request, 'posts/post_page.html', {'post': post})

@login_required(login_url="/users/login/")
def post_new(request):
  form = forms.CreatePost()  
  if request.method == "POST":
    form = forms.CreatePost(request.POST, request.FILES) 
    if form.is_valid():
      id = ObjectId()
      title = form.cleaned_data["title"]

      description = form.cleaned_data["description"]
      price = form.cleaned_data["price"]
      price = locale.currency(float(price), grouping=True)
      author = request.user.username 
      slug = str(id)

      date = datetime.now(timezone.utc) - timedelta(hours=6)


      database = client["marketplace"]
      collection = database["posts"]
      fs = gridfs.GridFS(database)

      image_file = request.FILES["image"]  
      if image_file:
        file_id = fs.put(image_file, filename=image_file.name)  
      else:
        file_id = None  
    
      new_post = {
          "_id": id,
          "title": title,
          "image": file_id,  
          "description": description,
          "price": price,
          "date": date, 
          "author": author,
          "slug": slug
      }

      collection.insert_one(new_post)
      return redirect("posts:list")
  return render(request, 'posts/post_new.html', {'form': form})


def get_image(request, image_id):
  database = client["marketplace"]
  fs = gridfs.GridFS(database)
  try:
      
      file = fs.get(ObjectId(image_id))
      response = HttpResponse(file.read(), content_type="image/jpeg") 
      response["Content-Disposition"] = f"inline; filename={file.filename}"
      return response
  except:
      return HttpResponse("Image not found", status=404)