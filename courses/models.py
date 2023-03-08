from django.db import models
from tinymce import models as tinymce_models

class Course(models.Model):
    title = models.CharField(max_length=60,null=False)
    title_img = models.ImageField(upload_to="courses/img", default="hacker.png")
    short_des = models.CharField(max_length=150)
    description = tinymce_models.HTMLField()
    price = models.FloatField(null=False)
    course_time = models.DateTimeField(null=False)
    meet_link = models.CharField(max_length=140, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title