from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Import views properly

app_name = 'posts'

urlpatterns = [
    path('home/', views.home_page, name="home"),  
    path('', views.posts_list, name="list"),  
    path('new-post/', views.post_new, name="new-post"),
    path('<slug:slug>/', views.post_page, name="page"),  
    path("images/<str:image_id>/", views.get_image, name="get_image"),  
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)