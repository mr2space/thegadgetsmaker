from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from purchase.models import FilePaymentInfo
from .forms import FileForm
from .models import Files
from home.templatetags import url


# upload file
def isTeacher(user):
    if user:
        status = user.groups.filter(name="teacher").count() > 0
        return status
    return False


def uploadFiles(request):
    param = url.setPara(request, "")
    if request.method != 'POST':
        param['form'] = FileForm()
        return render(request, "file/file_upload.html", param)
    form = FileForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/codes")
    return HttpResponse("<h1> Form not valid </h1>")


# show files
def showFiles(request):
    param = url.setPara(request, "")
    try:
        files = Files.objects.all().values()
        param['files'] = files
    except Exception as error:
        print("value not able to fetch", error)
    return render(request, "file/index.html", param)



# update the files



@login_required(login_url="/auth/")
@user_passes_test(isTeacher, login_url="/auth/")
def updateFiles(request,id):
    param = url.setPara(request, "")
    instance = get_object_or_404(Files, pk=id)
    if request.method != 'POST':
        param['form'] = FileForm(instance=instance)
        param["id"] = id
        return render(request, 'file/file_upload.html', param)
    form = FileForm(request.POST,request.FILES, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/codes')
    else:
        return HttpResponse("<h1> Form not valid </h1>")



def index(request,id):
    param = url.setPara(request, "Courses")
    try:
        file = Files.objects.get(id=id)
        param["file"] = file
        param['img_url'] = "/media/"

        param["show_payment_link"] = True
    except:
        print("course id not matched")
    try:
        user = User.objects.get(id=request.user.id)
        is_purchased = FilePaymentInfo.objects.get(course=file, user=user)
        param["show_payment_link"] = not (is_purchased.payment_completed)
        param["p"] = is_purchased
        print("purchased")
    except Exception as error:
        print(error)
    return render(request, "file/code.html", param)


