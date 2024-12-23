"""gadgetsmaker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include("home.urls")),
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
    path('courses/', include('courses.urls')),
    path('payment/', include('purchase.urls')),
    path('blogs/', include('blog.urls')),
    path('codes/', include('file.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# handler404 = "django_404_project.views.page_not_found_view"