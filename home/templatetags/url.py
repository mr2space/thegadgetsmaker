DEFAULT_URLS = {
    "Home": {
        "url": "",
        "status": '',
    },
    "Courses": {
        "url": "/courses",
        "status": '',
    },
    "My Learning": {
        "url": "/learning",
        "status": '',
    },


}

IMG_URL = "/media/"

def returnActiveUrl(urls=DEFAULT_URLS, active_url="Home"):
    url = urls[active_url]
    url['status'] = "active"
    return urls

