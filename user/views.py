from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from home.templatetags import url
from .authFiles.register import *
from .authFiles.log import *


# Create your views here.

def index(request):
    # TODO: AUTH PAGE
    param = url.setPara(request, "")
    return render(request, "user/index.html",param)


def login(request):
    if request.method != "POST":
        return redirect("/auth/")
    if logTheUser(request):
        return redirect("/courses/")
    param = url.setPara(request, "")
    param["page_msg"] = "username or password not matched"
    return render(request, "user/index.html", param)


@login_required(login_url="/auth/")
def test(request):
    return HttpResponse("welcome")


def logout(request):
    param = url.setPara(request, "")
    # TODO:LOGOUT PAGE
    if not request.user:
        return HttpResponse("user not logged")
    logoutUser(request)
    return redirect("/")


def registeration(request):
    param = url.setPara(request, "")
    if request.user.is_authenticated:
        param["page_msg"] = "logout to create new account"
        return redirect("/auth/")
    if request.method != "POST":
        print("not post")
        return redirect("/auth/")
    if savingUserModel(request):
        return redirect("/auth/")
    return redirect("/auth/otp")


@login_required(login_url="/auth/")
def otp(request):
    param = url.setPara(request, "")
    # TODO: OTP
    if request.method != "POST" :
        return render(request, "user/otp_verification.html",param)
    try:
        o = request.POST['otp']
        print(o,request.POST)
        int(o)
    except:
        print("failed int")
        param["page_msg"] = "invalid otp"
        return render(request, "user/otp_verification.html", param)
    try:
        if not request.user.is_authenticated:
            return redirect("/auth/")
    except:
        return redirect("/")
    try:
        saved_user = ExtendUser.objects.get(username=request.user.id)
    except Exception as error:
        print(request.user.id, "username not found !", error)
        return render(request, "error/500.html",param)

    if saved_user.otp == int(request.POST.get("otp")):
        try:
            ExtendUser.objects.filter(username=request.user.id).update(is_verified=True)
        except Exception as error:
            print("not able to update the verify flag", error)
            return render(request, "error/500.html")
        return redirect("/courses/")
    else:

        param["page_msg"] = "otp not matched"
        return render(request, "user/otp_verification.html", param)


@login_required(login_url="/auth/")
def resendOtp(request):
    # TODO : RESEND BUTTON
    # TODO: add this to url
    otp = otpGenerator()
    try:
        user = ExtendUser.objects.get(username=request.user.id)
    except Exception as error:
        print("Extend user not found")
    user.otp = otp
    user.save()
    SendEmailThread(otp=otp, username=request.user, email=user.email).start()
    return redirect("/auth/otp")
