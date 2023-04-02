from user.models import ExtendUser

DEFAULT_URLS = {
    "Home": {
        "url": "/",
        "status": '',
    },
    "Courses": {
        "url": "/courses",
        "status": '',
    },
    "My Learning": {
        "url": "/courses/my_learning",
        "status": '',
    },
    "Blog":{
        "url":"/blogs",
        "status":'',
    }
}

IMG_URL = "/media/"

def returnActiveUrl(urls={}, active_url="Home"):
    if not urls:
        urls = {
    "Home": {
        "url": "/",
        "status": '',
    },
    "Courses": {
        "url": "/courses",
        "status": '',
    },
    "My Learning": {
        "url": "/courses/my_learning",
        "status": '',
    },
    "Blog":{
        "url":"/blogs",
        "status":'',
    }
    }
    url = urls.get(active_url,{"status":False})
    url['status'] = "active"
    return urls



def setPara(request,page_name):
    param = {}
    extenduser = {}
    verified = False
    if request.user.is_authenticated:
        try:
            extenduser = ExtendUser.objects.get(username=request.user.id)
            verified = extenduser.is_verified
        except Exception as error:
            verified = False
    param["profile"] = {"url": "/profile"}
    param["urls"] = returnActiveUrl(active_url=page_name)
    param["user_info"] = extenduser
    param["img_url"] = IMG_URL
    param["verified"] = verified
    return param