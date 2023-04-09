from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.forms import ModelForm
from .models import Course
from django import forms


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title','title_img', 'short_des', 'description', 'price', 'course_time']
        widgets = {
            "course_time": DateTimePickerInput(),
        }
