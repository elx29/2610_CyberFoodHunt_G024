from django import forms
from .models import Post, Restaurant

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['restaurant_id', 'title', 'description', 'image']
        labels = {
            'restaurant_id': 'Restaurant',
            'title': 'Post Title',
            'description': 'Description',
            'image': 'Image URL or File Path',
        }