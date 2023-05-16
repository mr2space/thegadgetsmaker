from django.contrib.auth.models import Group
from django.shortcuts import render
from django.template.defaultfilters import register
from blog.models import Blog
from user.models import ExtendUser
from .templatetags import url




def index(request):
    param = url.setPara(request,"Home")
    blog = Blog.objects.all()[:4]
    param["blogs"] = blog
    return render(request, "home/home.html", param)


def cookie(request):
    return render(request, "pol/cookie_pol.html")

def page_not_found_view(request, exception):
    param = url.setPara(request, "")
    return render(request, 'home/404.html',param, status=404)
