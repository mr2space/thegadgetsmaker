from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

def fileFolder(instance, filename):
    return f"file/{instance.file_title}/{filename}"


class Files(models.Model):
    file_title = models.CharField(max_length=35)
    file_title_img = models.ImageField(upload_to=fileFolder)
    file = models.FileField(upload_to=fileFolder)
    short_desc = models.CharField(max_length=50)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.file_title
