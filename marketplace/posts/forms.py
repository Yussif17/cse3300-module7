from django import forms
from . import models

class CreatePost(forms.ModelForm):
  class Meta:
    model = models.Post
    fields = ["title", "price", "description", "image"]
    widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control title-class'}),
            'description': forms.Textarea(attrs={'class': 'form-control body-class', 'rows': 5}),
            'price': forms.TextInput(attrs={'class': 'form-control price-class'}),
            'image': forms.FileInput(attrs={'class': 'image-field'})
        }