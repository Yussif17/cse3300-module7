from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length=75, blank=False)
  description = models.TextField(max_length=10000, blank=False)
  price = models.DecimalField(max_digits=12, decimal_places=2 ,blank=False, default=0)
  slug = models.SlugField(unique=True, blank=True) 
  date = models.DateTimeField(auto_now_add=True)
  image = models.ImageField(default='fallback.png', blank=False)
  author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

  def save(self, *args, **kwargs):
    if not self.slug:  
        unique_id = str(uuid.uuid4())[:8]  
        self.slug = slugify(f"{self.title}-{unique_id}")
    super().save(*args, **kwargs)

  def __str__(self):
    return self.title
  