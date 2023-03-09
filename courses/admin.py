from django.contrib import admin
from .models import Course
# Register your models here.

# admin.site.register(Course)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    class Media:
        js = ('courses/tinyInject.js')