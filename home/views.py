from django.contrib.auth.models import Group
from django.shortcuts import render
from django.template.defaultfilters import register
from user.models import ExtendUser
from .templatetags import url




def index(request):
    param = {}
    verified = False
    extenduser = {}
    if request.user.is_authenticated:
        try:
            extenduser = ExtendUser.objects.get(username=request.user.id)
            verified = extenduser.is_verified
        except Exception as error:
            verified = False
    param["profile"] = {"url": "/profile"}
    param["urls"] = url.returnActiveUrl()
    param["user_info"] = extenduser
    param["img_url"] = url.IMG_URL
    print(extenduser)
    param["verified"] = verified
    return render(request, "base.html", param)
