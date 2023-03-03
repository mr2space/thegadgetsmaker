from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from home.templatetags import url
from .models import Course
from .form import CourseForm
from purchase.models import PaymentInfo



def index(request):
    param = {}
    try:
        courses = Course.objects.all().values()
        param['courses']=courses
        param['img_url']="/media/"
        print(courses[0])
    except Exception as error:
        print("value not able to fetch", error)
    param["urls"] = url.returnActiveUrl(active_url="Courses")
    return render(request, "courses/index.html", param)


def isTeacher(user):
    if user:
        status = user.groups.filter(name="teacher").count() > 0
        return status
    return False


@login_required(login_url="/auth/")
@user_passes_test(isTeacher, login_url="/auth/")
def new(request):
    param = {}
    #TODO:URL ACTIVE
    if request.method != 'POST':
        param['form'] = CourseForm()
        print("here")
        return render(request, "courses/new_course.html", param)
    form = CourseForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse("course created")
    return HttpResponse("form not valid")


def coursePage(request, id):
    param = {}
    try:
        course = Course.objects.get(id=id)
        param["course"] = course
        param['img_url'] = "/media/"
        param["show_payment_link"] = True
    except:
        print("course id not matched")
    try:
        user = User.objects.get(id=request.user.id)
        is_purchased = PaymentInfo.objects.get(course=course, user=user)
        param["show_payment_link"] = not(is_purchased.payment_completed)
        param["meet"] = course.meet_link
        print("purchased")
    except Exception as error:
        print(error)
        pass
    param["urls"] = url.returnActiveUrl(active_url="Courses")
    return render(request, "courses/course.html", param)