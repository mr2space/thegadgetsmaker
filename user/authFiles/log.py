from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def logTheUser(request):
    user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
    if user:
        login(request, user)
    else:
        print("failed to login")
    return user

def logoutUser(request):
    logout(request)
    return 0