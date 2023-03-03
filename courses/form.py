from django.forms import ModelForm
from .models import Course


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title','title_img', 'short_des', 'description', 'price', 'course_time']
