from django.forms import ModelForm
from .models import Files

class FileForm(ModelForm):
    class Meta:
        model = Files
        fields = ['file_title','file_title_img', 'file', 'short_desc', 'price']