from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .authFiles.register import *
from .authFiles.log import *


# Create your views here.

def index(request):
    return render(request, "user/index.html")


def login(request):
    if request.method != "POST":
        return redirect("/auth/")
    if logTheUser(request):
        return redirect("/courses/")
    return HttpResponse("failed")


@login_required(login_url="/auth/")
def test(request):
    return HttpResponse("welcome")

def logout(request):
    if not request.user:
        return HttpResponse("user not logged")
    logoutUser(request)
    return HttpResponse("user logout ")


def registeration(request):
    if request.method != "POST":
        print("not post")
        return redirect("/auth/")
    if  savingUserModel(request):
        return HttpResponse("not user saved")
    return redirect("/auth/otp")


@login_required(login_url="/auth/")
def otp(request):
    if request.method != "POST":
        return render(request, "user/otp_verification.html")
    try:
        if not request.user.is_authenticated:
            return redirect("/auth/")
    except:
        return redirect("/")
    try:
        saved_user = ExtendUser.objects.get(username=request.user.id)
        print(saved_user)
    except Exception as error:
        print(request.user.id, "username not found !", error)
        return redirect("/auth/")

    if saved_user.otp == int(request.POST.get("otp")):
        try:
            ExtendUser.objects.filter(username=request.user.id).update(is_verified=True)
        except Exception as error:
            print("not able to update the verify flag", error)
            return redirect("/auth/otp/")
        return redirect("/courses/")
    else:
        HttpResponse("otp failed")


@login_required(login_url="/auth/")
def resendOtp(request):
    # TODO: add this to url
    if request.method != 'POST':
        print('not post method')
        return redirect("/auth/otp")
    otp = otpGenerator()
    ExtendUser.objects.filter(username=request.user.id).first().update(opt=otp)
    sendEmail(otp, request)
    return redirect("/auth/otp")
