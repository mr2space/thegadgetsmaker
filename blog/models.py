from django.db import models
from tinymce import models as tinymce_models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=60, null=False)
    title_img = models.ImageField(upload_to="blog/title/img", default="hacker.png")
    short_des = models.CharField(max_length=150)
    body = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
