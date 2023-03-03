from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="courses"),
    path('new/', views.new, name="add course"),
    path('course/<int:id>', views.coursePage, name="course page"),
]