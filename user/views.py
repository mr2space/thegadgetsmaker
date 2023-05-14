from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from home.templatetags import url
from .authFiles.register import *
from .authFiles.log import *
from django.contrib.auth.models import User , Group

# Create your views here.

def index(request):
    # TODO: AUTH PAGE
    msg = request.GET.get("msg", None)
    param = url.setPara(request, "")
    param['page_msg'] = msg
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
        return redirect(f"/auth/?msg={param['page_msg']}")
    if request.method != "POST":
        print("not post")
        return redirect("/auth/")
    obj = savingUserModel(request)
    if obj[0]:
        param["page_msg"] = obj[1]
        return render(request, "user/index.html",param)
    #TODO: REDIRECT TO /AUTH/OTP
    return redirect("/auth/otp")


@login_required(login_url="/auth/")
def otp(request):
    param = url.setPara(request, "")
    # TODO: OTP
    o = -1
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
            user = User.objects.get(username=request.user)
            group = Group.objects.get(name="user")
            user.groups.add(group)
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
    SendEmailThread(otp=otp, username=request.user, email=request.user.email).start()
    return redirect("/auth/otp")
