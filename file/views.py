from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import FileForm
from .models import Files
from home.templatetags import url


# upload file

def uploadFiles(request):
    param = url.setPara(request, "")
    if request.method != 'POST':
        param['form'] = FileForm()
        return render(request, "file/file_upload.html", param)
    form = FileForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse("file created")
    return HttpResponse("form not valid")


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

