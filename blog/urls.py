from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="blogs"),
    path('new/',views.addArtical, name="new blog"),
    path('blog/<int:id>',views.showBlog, name="blog"),
]