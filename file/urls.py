from django.urls import path
from . import views
urlpatterns = [
    path("", views.showFiles, name="files"),
    path("new", views.uploadFiles, name="file_upload"),
    path("update/<int:id>",views.updateFiles,name="update_files")

]