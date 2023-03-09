from django.forms import ModelForm
from .models import Blog


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['title','title_img', 'short_des', 'body']