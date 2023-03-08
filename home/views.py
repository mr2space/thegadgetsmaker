from django.contrib.auth.models import Group
from django.shortcuts import render
from django.template.defaultfilters import register
from user.models import ExtendUser
from .templatetags import url




def index(request):
    param = url.setPara(request,"Home")
    return render(request, "base.html", param)
